"""Command-line interface for token counter."""

import click
import sys
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .counter import TokenCounter
from .models import SupportedModels, Provider


console = Console()

# Default latest models for 2026
DEFAULT_LATEST_MODELS = [
    # OpenAI GPT-5 series
    'gpt-5',
    'gpt-5.2',
    # Anthropic Claude 4.5 series
    'claude-opus-4.5',
    'claude-sonnet-4.5',
    'claude-haiku-4.5',
    # Google Gemini 3 series
    'gemini-3-pro',
    'gemini-3-flash',
]


def read_text_from_source(text: Optional[str], file: Optional[str],
                         files: Optional[List[str]]) -> List[str]:
    """Read text from various sources."""
    texts = []

    if text:
        texts.append(text)

    if file:
        try:
            texts.append(Path(file).read_text(encoding='utf-8'))
        except Exception as e:
            console.print(f"[red]Error reading file {file}: {e}[/red]")
            sys.exit(1)

    if files:
        for f in files:
            try:
                texts.append(Path(f).read_text(encoding='utf-8'))
            except Exception as e:
                console.print(f"[red]Error reading file {f}: {e}[/red]")

    # If no text provided, read from stdin
    if not texts and not sys.stdin.isatty():
        texts.append(sys.stdin.read())

    if not texts:
        console.print("[red]No text provided. Use --text, --file, or pipe text via stdin.[/red]")
        sys.exit(1)

    return texts


def format_cost(cost: float) -> str:
    """Format cost with appropriate precision."""
    if cost < 0.01:
        return f"${cost:.6f}"
    elif cost < 1:
        return f"${cost:.4f}"
    else:
        return f"${cost:.2f}"


@click.command()
@click.option('--text', '-t', help='Text to count tokens for')
@click.option('--file', '-f', help='File to read text from')
@click.option('--files', '-F', multiple=True, help='Multiple files to process')
@click.option('--model', '-m', default='',
              help='Comma-separated list of models (e.g., gpt-4,claude-3-opus). If not specified, shows all latest models.')
@click.option('--list-models', is_flag=True, help='List all supported models')
@click.option('--estimate-cost', '-c', is_flag=True,
              help='Estimate cost for processing the text')
@click.option('--output-tokens', '-o', type=int,
              help='Number of expected output tokens for cost estimation')
@click.option('--check-limit', '-l', is_flag=True,
              help='Check if text exceeds model token limit')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--format', type=click.Choice(['text', 'json', 'table']),
              default='text', help='Output format')
def main(text: Optional[str], file: Optional[str], files: Optional[List[str]],
         model: str, list_models: bool, estimate_cost: bool,
         output_tokens: Optional[int], check_limit: bool,
         verbose: bool, format: str):
    """Token Counter - Count tokens for various LLM providers.

    Examples:

    \b
    # Count tokens for text
    token-counter -t "Hello, world!" -m gpt-4

    \b
    # Count tokens from file
    token-counter -f document.txt -m claude-3-opus

    \b
    # Compare multiple models (comma-separated)
    token-counter -t "Your text here" -m gpt-4,claude-3-opus,gemini-3-pro

    \b
    # Show all latest models (no -m flag)
    token-counter -t "Your text here"

    \b
    # Estimate costs across models
    token-counter -t "Your text here" -m gpt-4,gpt-4-turbo -c

    \b
    # Check token limit
    token-counter -f large_document.txt -m gpt-3.5-turbo -l

    \b
    # Process multiple files with multiple models
    token-counter -F file1.txt -F file2.txt -m gpt-4,claude-3-haiku
    """
    if list_models:
        show_models_list()
        return

    try:
        # Read text from various sources
        texts = read_text_from_source(text, file, files)

        # Process each model
        if model:
            # Parse comma-separated models
            models_to_process = [m.strip() for m in model.split(',') if m.strip()]
        else:
            # Use all latest models by default
            models_to_process = DEFAULT_LATEST_MODELS

        results = {}

        for model_name in models_to_process:
            # Initialize counter for this model
            counter = TokenCounter(model_name)

            # Count tokens
            total_tokens = sum(counter.count_tokens(t) for t in texts)

            # Store results for this model
            results[model_name] = {
                'counter': counter,
                'total_tokens': total_tokens
            }

        if format == 'json':
            import json
            output = {"models": {}}

            for model_name, data in results.items():
                model_result = {"total_tokens": data['total_tokens']}

                if estimate_cost:
                    cost_data = data['counter'].estimate_cost(texts,
                                                     include_output=bool(output_tokens),
                                                     output_tokens=output_tokens)
                    model_result.update(cost_data)

                if check_limit:
                    limit_data = data['counter'].check_token_limit(texts)
                    model_result.update(limit_data)

                output["models"][model_name] = model_result

            console.print(json.dumps(output, indent=2))

        elif format == 'table':
            if len(results) == 1:
                # Single model - use original format
                model_name = list(results.keys())[0]
                data = results[model_name]
                table = Table(title=f"Token Count Analysis - {model_name}")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="green")

                table.add_row("Model", model_name)
                table.add_row("Total Tokens", str(data['total_tokens']))

                if estimate_cost:
                    cost_data = data['counter'].estimate_cost(texts,
                                                     include_output=bool(output_tokens),
                                                     output_tokens=output_tokens)
                    table.add_row("Input Cost", format_cost(cost_data['input_cost']))

                    if 'output_cost' in cost_data:
                        table.add_row("Output Tokens", str(cost_data['output_tokens']))
                        table.add_row("Output Cost", format_cost(cost_data['output_cost']))
                        table.add_row("Total Cost", format_cost(cost_data['total_cost']))

                if check_limit:
                    limit_data = data['counter'].check_token_limit(texts)
                    table.add_row("Token Limit", str(limit_data['limit']))
                    table.add_row("Usage", f"{limit_data['percentage_used']}%")
                    if limit_data['exceeds_limit']:
                        table.add_row("Status", "[red]EXCEEDS LIMIT[/red]")
                    else:
                        table.add_row("Status", "[green]Within Limit[/green]")
            else:
                # Multiple models - comparison table
                table = Table(title="Token Count Analysis - Model Comparison")
                table.add_column("Model", style="cyan")
                table.add_column("Total Tokens", style="green")

                if estimate_cost:
                    table.add_column("Input Cost", style="yellow")
                    if output_tokens:
                        table.add_column("Output Cost", style="yellow")
                        table.add_column("Total Cost", style="magenta")

                if check_limit:
                    table.add_column("Token Limit", style="blue")
                    table.add_column("Usage %", style="blue")
                    table.add_column("Status", style="blue")

                for model_name, data in sorted(results.items()):
                    row = [model_name, str(data['total_tokens'])]

                    if estimate_cost:
                        cost_data = data['counter'].estimate_cost(texts,
                                                         include_output=bool(output_tokens),
                                                         output_tokens=output_tokens)
                        row.append(format_cost(cost_data['input_cost']))
                        if output_tokens:
                            row.append(format_cost(cost_data['output_cost']))
                            row.append(format_cost(cost_data['total_cost']))

                    if check_limit:
                        limit_data = data['counter'].check_token_limit(texts)
                        row.append(str(limit_data['limit']))
                        row.append(f"{limit_data['percentage_used']}%")
                        if limit_data['exceeds_limit']:
                            row.append("[red]EXCEEDS[/red]")
                        else:
                            row.append("[green]OK[/green]")

                    table.add_row(*row)

            console.print(table)

        else:  # text format
            if verbose and len(texts) > 1:
                console.print(f"[cyan]Files processed:[/cyan] {len(texts)}")

            for i, (model_name, data) in enumerate(sorted(results.items())):
                if len(results) > 1:
                    if i > 0:
                        console.print()  # Add spacing between models
                    console.print(f"[bold cyan]--- {model_name} ---[/bold cyan]")
                else:
                    console.print(f"[cyan]Model:[/cyan] {model_name}")

                console.print(f"[cyan]Total tokens:[/cyan] {data['total_tokens']:,}")

                # Cost estimation
                if estimate_cost:
                    cost_data = data['counter'].estimate_cost(texts,
                                                     include_output=bool(output_tokens),
                                                     output_tokens=output_tokens)
                    console.print(f"\n[yellow]Cost Estimation:[/yellow]")
                    console.print(f"  Input tokens: {cost_data['input_tokens']:,}")
                    console.print(f"  Input cost: {format_cost(cost_data['input_cost'])}")

                    if 'output_cost' in cost_data:
                        console.print(f"  Output tokens: {cost_data['output_tokens']:,}")
                        console.print(f"  Output cost: {format_cost(cost_data['output_cost'])}")
                        console.print(f"  [bold]Total cost: {format_cost(cost_data['total_cost'])}[/bold]")

                # Token limit check
                if check_limit:
                    limit_data = data['counter'].check_token_limit(texts)
                    console.print(f"\n[yellow]Token Limit Check:[/yellow]")
                    console.print(f"  Model limit: {limit_data['limit']:,} tokens")
                    console.print(f"  Usage: {limit_data['percentage_used']}%")

                    if limit_data['exceeds_limit']:
                        console.print("  [red bold]⚠ Text exceeds model token limit![/red bold]")
                    else:
                        console.print(f"  [green]✓ Within limit[/green] ({limit_data['tokens']:,}/{limit_data['limit']:,})")

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


def show_models_list():
    """Display list of supported models."""
    table = Table(title="Supported Models")
    table.add_column("Provider", style="cyan")
    table.add_column("Model", style="green")
    table.add_column("Max Tokens", style="yellow")
    table.add_column("Input Cost/1K", style="magenta")
    table.add_column("Output Cost/1K", style="magenta")

    # Group by provider
    for provider in Provider:
        models = SupportedModels.get_provider_models(provider)
        for name, config in sorted(models.items()):
            output_cost = format_cost(config.output_cost_per_1k) if config.output_cost_per_1k else "N/A"
            table.add_row(
                provider.value.capitalize(),
                name,
                f"{config.max_tokens:,}",
                format_cost(config.input_cost_per_1k),
                output_cost
            )

    console.print(table)


if __name__ == '__main__':
    main()