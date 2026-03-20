"""CLI interface for AI Knowledge Assistant"""

import asyncio
import logging
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

from src.config import Settings, LogConfig
from src.ai_assistant import AIAssistant
from src.ai_assistant.document_processor import DocumentProcessor

# Setup CLI
console = Console()
LogConfig.setup_logging("INFO", "text")
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """AI Knowledge Assistant CLI"""
    pass


@cli.command()
@click.option("--file", type=click.Path(exists=True), help="Document file path")
@click.option("--text", type=str, help="Text content")
@click.option("--source", type=str, default="cli", help="Document source")
def add_document(file: Optional[str], text: Optional[str], source: str):
    """Add document to knowledge base
    
    Args:
        file: Path to document file
        text: Text content
        source: Document source
    """
    try:
        settings = Settings()
        
        with console.status("[bold green]Initializing assistant..."):
            assistant_sync = asyncio.run(_get_assistant(settings))
        
        if file:
            content = Path(file).read_text()
            source = source or Path(file).name
            console.print(f"[green]Loaded file: {file}")
        elif text:
            content = text
        else:
            console.print("[red]Error: Provide either --file or --text")
            return
        
        with console.status("[bold green]Processing document..."):
            docs = [{"content": content, "source": source}]
            texts, metadata = DocumentProcessor.process_documents(docs)
            doc_ids = asyncio.run(assistant_sync.add_documents(texts, metadata))
        
        console.print(f"[green]✓ Added {len(doc_ids)} document chunks")
        console.print(f"[cyan]Document IDs: {', '.join(doc_ids[:3])}{'...' if len(doc_ids) > 3 else ''}")
    
    except Exception as e:
        console.print(f"[red]Error: {e}", style="bold")


@cli.command()
@click.option("--query", type=str, prompt="Enter query", help="User query")
@click.option("--top-k", type=int, default=5, help="Number of results")
@click.option("--stream", is_flag=True, help="Stream response")
def query(query: str, top_k: int, stream: bool):
    """Query the knowledge base
    
    Args:
        query: User query
        top_k: Number of results
        stream: Stream response
    """
    try:
        settings = Settings()
        
        with console.status("[bold green]Initializing assistant..."):
            assistant_sync = asyncio.run(_get_assistant(settings))
        
        with console.status("[bold green]Searching knowledge base..."):
            result = asyncio.run(assistant_sync.query(query, top_k, stream))
        
        console.print("\n[bold cyan]Answer:[/bold cyan]")
        console.print(result["answer"])
        
        console.print("\n[bold cyan]Sources:[/bold cyan]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Score", style="cyan")
        table.add_column("Source", style="green")
        
        for source in result["sources"]:
            table.add_row(
                f"{source['score']:.2f}",
                source["text"],
            )
        
        console.print(table)
        console.print(f"\n[cyan]Confidence: {result['confidence']:.2f}")
    
    except Exception as e:
        console.print(f"[red]Error: {e}", style="bold")


@cli.command()
def stats():
    """Show assistant statistics"""
    try:
        settings = Settings()
        
        with console.status("[bold green]Initializing assistant..."):
            assistant_sync = asyncio.run(_get_assistant(settings))
        
        with console.status("[bold green]Fetching statistics..."):
            stats_data = asyncio.run(assistant_sync.get_stats())
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in stats_data.items():
            table.add_row(key, str(value))
        
        console.print(table)
    
    except Exception as e:
        console.print(f"[red]Error: {e}", style="bold")


async def _get_assistant(settings: Settings) -> AIAssistant:
    """Get or create assistant instance"""
    return AIAssistant(settings)


if __name__ == "__main__":
    cli()
