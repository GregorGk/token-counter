#!/usr/bin/env python3
"""
Batch token counter for processing multiple files with Gemini 3.0, Claude Opus 4.5, and ChatGPT 5.2.

Usage: python batch_token_counter.py *.txt
"""

import sys
import glob
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add the token_counter package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from token_counter import TokenCounter

console = Console()

# Target models
TARGET_MODELS = ["gemini-3.0", "claude-opus-4.5", "chatgpt-5.2"]


def process_files(file_patterns):
    """Process multiple files and generate a summary report."""
    files = []
    for pattern in file_patterns:
        files.extend(glob.glob(pattern))

    if not files:
        console.print("[red]No files found matching the patterns.[/red]")
        return

    console.print(f"[cyan]Found {len(files)} files to process[/cyan]")

    # Summary table
    summary_table = Table(title="Batch Token Count Summary", show_header=True, header_style="bold cyan")
    summary_table.add_column("File", style="green", width=30)
    summary_table.add_column("Size (KB)", justify="right", style="white")

    for model in TARGET_MODELS:
        summary_table.add_column(f"{model}\nTokens", justify="right", style="yellow")

    summary_table.add_column("Avg Tokens", justify="right", style="magenta")

    total_tokens_by_model = {model: 0 for model in TARGET_MODELS}
    file_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing files...", total=len(files))

        for file_path in files:
            try:
                path = Path(file_path)
                text = path.read_text(encoding='utf-8')
                size_kb = path.stat().st_size / 1024

                tokens_by_model = {}
                for model in TARGET_MODELS:
                    try:
                        counter = TokenCounter(model)
                        tokens = counter.count_tokens(text)
                        tokens_by_model[model] = tokens
                        total_tokens_by_model[model] += tokens
                    except Exception as e:
                        tokens_by_model[model] = -1

                avg_tokens = sum(t for t in tokens_by_model.values() if t > 0) / len([t for t in tokens_by_model.values() if t > 0])

                row_data = [path.name, f"{size_kb:.1f}"]
                for model in TARGET_MODELS:
                    token_count = tokens_by_model.get(model, -1)
                    row_data.append(f"{token_count:,}" if token_count > 0 else "Error")
                row_data.append(f"{int(avg_tokens):,}")

                summary_table.add_row(*row_data)
                file_count += 1

            except Exception as e:
                console.print(f"[red]Error processing {file_path}: {e}[/red]")

            progress.update(task, advance=1)

    console.print()
    console.print(summary_table)

    # Total summary
    if file_count > 0:
        console.print("\n[bold cyan]Total Token Summary:[/bold cyan]")
        total_table = Table(show_header=True, header_style="bold")
        total_table.add_column("Model", style="green")
        total_table.add_column("Total Tokens", justify="right", style="yellow")
        total_table.add_column("Avg Tokens/File", justify="right", style="magenta")

        for model in TARGET_MODELS:
            total = total_tokens_by_model[model]
            avg = total / file_count if file_count > 0 else 0
            total_table.add_row(model, f"{total:,}", f"{int(avg):,}")

        console.print(total_table)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[red]Usage: python batch_token_counter.py file1.txt file2.txt ...[/red]")
        console.print("[yellow]   or: python batch_token_counter.py *.txt[/yellow]")
        sys.exit(1)

    process_files(sys.argv[1:])