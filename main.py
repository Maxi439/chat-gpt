#!/usr/bin/env python3
"""
Tax Content Workflow Agent
Automatisierter Multi-Agenten-Content-Workflow für steuerliche Investment-Themen.

Verwendung:
  python main.py generate --topic "Investitionsabzugsbetrag §7g EStG"
  python main.py schedule --short video_reel.mp4 --long video_youtube.mp4
  python main.py metrics
  python main.py top
"""
import logging
import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from database.db import init_db
from agents.content_orchestrator import produce_content
from workflow.pipeline import run_content_pipeline
from workflow.scheduler import start_scheduler
from workflow.tracker import collect_metrics, top_performers
from database.db import get_session
from database.models import ContentItem
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

console = Console()


@click.group()
def cli():
    """Tax Content Workflow Agent – steuerlicher Investment-Content auf Autopilot."""
    init_db()


@cli.command()
@click.option("--topic", default=None, help="Steuer-Thema (leer = erstes aus der Topic-Liste)")
@click.option("--dry-run", is_flag=True, default=True, help="Nur Content generieren, nicht posten")
@click.option("--short", default="", help="Pfad zum Short-Video (TikTok/Instagram)")
@click.option("--long", default="", help="Pfad zum Long-Video (YouTube)")
def generate(topic, dry_run, short, long):
    """Generiert Content für ein Thema (und veröffentlicht optional)."""
    if not topic:
        topic = config.TAX_TOPICS[0]

    console.rule(f"[bold blue]Thema: {topic}")
    result = run_content_pipeline(
        topic=topic,
        video_short_path=short,
        video_long_path=long,
        dry_run=dry_run or (not short),
    )

    with get_session() as session:
        item = session.get(ContentItem, result["content_item_id"])
        _print_content_summary(item)

    if not dry_run and short:
        console.print("\n[bold green]Veröffentlichungsergebnisse:")
        for platform, info in result["platforms"].items():
            icon = "✓" if info["success"] else "✗"
            console.print(f"  {icon} {platform}: {info.get('post_id') or info.get('error')}")


@cli.command()
@click.option("--short", default="", help="Pfad zum Short-Video (TikTok/Instagram)")
@click.option("--long", default="", help="Pfad zum Long-Video (YouTube)")
def schedule(short, long):
    """Startet den automatisierten Scheduler (3× pro Woche)."""
    days = [["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][d] for d in config.POSTING_DAYS]
    console.print(
        f"[bold]Scheduler gestartet[/bold] – "
        f"Posting an {', '.join(days)} um {config.POSTING_TIME_UTC} UTC"
    )
    start_scheduler(video_short_path=short, video_long_path=long)


@cli.command()
def metrics():
    """Holt aktuelle Performance-Metriken von allen Plattformen."""
    console.print("[bold]Metriken werden abgerufen...")
    summary = collect_metrics()
    if not summary:
        console.print("[yellow]Keine veröffentlichten Posts mit Metriken gefunden.")
        return

    table = Table(title="Performance Metriken", show_lines=True)
    table.add_column("Plattform", style="cyan")
    table.add_column("Post ID", style="dim")
    table.add_column("Views", justify="right")
    table.add_column("Engagement %", justify="right", style="green")
    for row in summary:
        table.add_row(
            row["platform"], row["post_id"],
            str(row["views"]), f"{row['engagement_rate']:.2f}%"
        )
    console.print(table)


@cli.command()
@click.option("--limit", default=5, help="Anzahl Top-Posts")
def top(limit):
    """Zeigt die Top-Posts nach Engagement-Rate."""
    performers = top_performers(limit=limit)
    if not performers:
        console.print("[yellow]Keine Metriken vorhanden.")
        return

    table = Table(title=f"Top {limit} Posts", show_lines=True)
    table.add_column("Plattform", style="cyan")
    table.add_column("Views", justify="right")
    table.add_column("Likes", justify="right")
    table.add_column("Engagement %", justify="right", style="bold green")
    table.add_column("Gemessen am")
    for p in performers:
        table.add_row(
            p["platform"], str(p["views"]), str(p["likes"]),
            f"{p['engagement_rate']:.2f}%", p["measured_at"]
        )
    console.print(table)


def _print_content_summary(item: ContentItem) -> None:
    if not item:
        return
    console.rule("[bold green]Generierter Content")
    console.print(f"[bold]Titel:[/bold] {item.title}")
    console.print(f"\n[bold]Short-Skript (TikTok/Reel):[/bold]\n{item.script_short}")
    console.print(f"\n[bold]Instagram Caption:[/bold]\n{item.caption_instagram}")
    console.print(f"\n[bold]TikTok Caption:[/bold]\n{item.caption_tiktok}")
    console.print(f"\n[bold]Thumbnail-Prompt:[/bold]\n{item.thumbnail_prompt}")
    console.print(f"\n[bold]Instagram Hashtags:[/bold] {' '.join(item.hashtags_instagram or [])}")
    console.print(f"\n[bold]TikTok Hashtags:[/bold] {' '.join(item.hashtags_tiktok or [])}")
    console.print(f"\n[bold]YouTube Tags:[/bold] {', '.join(item.tags_youtube or [])}")


if __name__ == "__main__":
    cli()
