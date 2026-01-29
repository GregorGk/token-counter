#!/usr/bin/env python3
"""
Script to count tokens for Gemini 3.0, Claude Opus 4.5, and ChatGPT 5.2 from a text file.

Usage: python count_tokens_for_file.py input.txt
"""

import sys
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Add the token_counter package to the path
sys.path.insert(0, str(Path(__file__).parent))

from token_counter import TokenCounter


console = Console()


# Target models
TARGET_MODELS = ["gemini-3.0", "claude-opus-4.5", "chatgpt-5.2"]


def format_number(num: int) -> str:
    """Format number with thousand separators."""
    return f"{num:,}"


def format_cost(cost: float) -> str:
    """Format cost with appropriate precision."""
    if cost < 0.01:
        return f"${cost:.6f}"
    elif cost < 1:
        return f"${cost:.4f}"
    else:
        return f"${cost:.2f}"


def read_file(file_path: Path) -> str:
    """Read content from a text file."""
    try:
        return file_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        console.print(f"[red]Error: File '{file_path}' not found.[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        sys.exit(1)


def analyze_text(text: str) -> dict:
    """Analyze text statistics."""
    lines = text.split('\n')
    words = text.split()
    chars = len(text)

    return {
        "characters": chars,
        "words": len(words),
        "lines": len(lines),
        "avg_word_length": round(sum(len(word) for word in words) / len(words), 2) if words else 0
    }


def count_tokens_for_models(text: str, models: list[str]) -> dict:
    """Count tokens for specified models."""
    results = {}

    for model_name in models:
        try:
            counter = TokenCounter(model_name)
            token_count = counter.count_tokens(text)
            cost_data = counter.estimate_cost(text, include_output=True)
            limit_check = counter.check_token_limit(text)

            results[model_name] = {
                "tokens": token_count,
                "input_cost": cost_data["input_cost"],
                "output_cost": cost_data.get("output_cost", 0),
                "total_cost": cost_data.get("total_cost", cost_data["input_cost"]),
                "max_tokens": counter.model_config.max_tokens,
                "percentage_used": limit_check["percentage_used"],
                "exceeds_limit": limit_check["exceeds_limit"]
            }
        except Exception as e:
            console.print(f"[yellow]Warning: Error processing {model_name}: {e}[/yellow]")
            results[model_name] = None

    return results


def display_results(file_path: Path, text: str, text_stats: dict, results: dict):
    """Display results in a formatted table."""
    # File info panel
    file_info = Panel(
        f"[cyan]File:[/cyan] {file_path.name}\n"
        f"[cyan]Size:[/cyan] {file_path.stat().st_size:,} bytes\n"
        f"[cyan]Characters:[/cyan] {format_number(text_stats['characters'])}\n"
        f"[cyan]Words:[/cyan] {format_number(text_stats['words'])}\n"
        f"[cyan]Lines:[/cyan] {format_number(text_stats['lines'])}\n"
        f"[cyan]Avg word length:[/cyan] {text_stats['avg_word_length']} chars",
        title="File Statistics",
        expand=False
    )
    console.print(file_info)
    console.print()

    # Token count table
    table = Table(title="Token Count Analysis", show_header=True, header_style="bold cyan")
    table.add_column("Model", style="green", width=20)
    table.add_column("Tokens", justify="right", style="yellow")
    table.add_column("Max Tokens", justify="right", style="white")
    table.add_column("Usage", justify="right", style="magenta")
    table.add_column("Input Cost", justify="right", style="blue")
    table.add_column("Output Cost", justify="right", style="blue")
    table.add_column("Total Cost", justify="right", style="bold blue")
    table.add_column("Status", justify="center")

    for model_name in TARGET_MODELS:
        if results.get(model_name):
            data = results[model_name]
            status = "[red]⚠ EXCEEDS[/red]" if data["exceeds_limit"] else "[green]✓ OK[/green]"

            table.add_row(
                model_name,
                format_number(data["tokens"]),
                format_number(data["max_tokens"]),
                f"{data['percentage_used']:.1f}%",
                format_cost(data["input_cost"]),
                format_cost(data["output_cost"]),
                format_cost(data["total_cost"]),
                status
            )
        else:
            table.add_row(
                model_name,
                "[red]Error[/red]",
                "-",
                "-",
                "-",
                "-",
                "-",
                "[red]Failed[/red]"
            )

    console.print(table)

    # Summary
    console.print("\n[bold cyan]Summary:[/bold cyan]")

    # Find model with lowest token count
    valid_results = {k: v for k, v in results.items() if v is not None}
    if valid_results:
        min_tokens_model = min(valid_results.items(), key=lambda x: x[1]["tokens"])
        max_tokens_model = max(valid_results.items(), key=lambda x: x[1]["tokens"])
        cheapest_model = min(valid_results.items(), key=lambda x: x[1]["total_cost"])

        console.print(f"• Most efficient tokenization: [green]{min_tokens_model[0]}[/green] ({format_number(min_tokens_model[1]['tokens'])} tokens)")
        console.print(f"• Least efficient tokenization: [yellow]{max_tokens_model[0]}[/yellow] ({format_number(max_tokens_model[1]['tokens'])} tokens)")
        console.print(f"• Most cost-effective: [green]{cheapest_model[0]}[/green] ({format_cost(cheapest_model[1]['total_cost'])})")

        # Token ratio comparison
        if min_tokens_model[1]["tokens"] > 0:
            ratio = max_tokens_model[1]["tokens"] / min_tokens_model[1]["tokens"]
            console.print(f"• Token efficiency ratio: [yellow]{ratio:.2f}x[/yellow] difference between models")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Count tokens for Gemini 3.0, Claude Opus 4.5, and ChatGPT 5.2 from a text file."
    )
    parser.add_argument("file", type=Path, help="Path to the text file")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--csv", action="store_true", help="Output results as CSV")

    args = parser.parse_args()

    # Check if file exists
    if not args.file.exists():
        console.print(f"[red]Error: File '{args.file}' does not exist.[/red]")
        sys.exit(1)

    if not args.file.suffix == '.txt':
        console.print(f"[yellow]Warning: File '{args.file}' is not a .txt file. Proceeding anyway...[/yellow]")

    # Read file content
    console.print(f"[cyan]Reading file:[/cyan] {args.file}")
    text = read_file(args.file)

    # Analyze text
    text_stats = analyze_text(text)

    # Count tokens for each model
    console.print(f"[cyan]Counting tokens for models:[/cyan] {', '.join(TARGET_MODELS)}")
    console.print()

    results = count_tokens_for_models(text, TARGET_MODELS)

    # Display results
    if args.json:
        import json
        output = {
            "file": str(args.file),
            "text_statistics": text_stats,
            "models": results
        }
        console.print(json.dumps(output, indent=2))
    elif args.csv:
        console.print("Model,Tokens,MaxTokens,Usage%,InputCost,OutputCost,TotalCost,ExceedsLimit")
        for model_name in TARGET_MODELS:
            if results.get(model_name):
                data = results[model_name]
                console.print(f"{model_name},{data['tokens']},{data['max_tokens']},"
                            f"{data['percentage_used']},{data['input_cost']},"
                            f"{data['output_cost']},{data['total_cost']},{data['exceeds_limit']}")
    else:
        display_results(args.file, text, text_stats, results)


if __name__ == "__main__":
    main()