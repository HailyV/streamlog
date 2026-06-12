"""streamlog — Twitch session tracker CLI"""

from __future__ import annotations

from typing import Annotated, Optional
import typer

from streamlog import storage, display

app = typer.Typer(
    name="streamlog",
    help="🎮 track your twitch streams from the terminal",
    no_args_is_help=True,
    rich_markup_mode="rich",
    pretty_exceptions_show_locals=False,
)


@app.command()
def log(
    game: Annotated[str, typer.Option("--game", "-g", help="game you streamed", prompt="🎮 game")] = "",
    duration: Annotated[
        int,
        typer.Option("--duration", "-d", help="stream duration in minutes", prompt="⏱  duration (minutes)"),
    ] = 0,
    peak: Annotated[
        int,
        typer.Option("--peak", "-p", help="peak viewer count", prompt="👀 peak viewers"),
    ] = 0,
    avg: Annotated[
        int,
        typer.Option("--avg", "-a", help="average viewer count", prompt="📊 avg viewers"),
    ] = 0,
    clips: Annotated[
        int,
        typer.Option("--clips", "-c", help="number of clips made", prompt="✂️  clips made"),
    ] = 0,
    followers: Annotated[
        int,
        typer.Option("--followers", "-f", help="new followers gained", prompt="➕ new followers"),
    ] = 0,
    vibe: Annotated[
        str,
        typer.Option(
            "--vibe",
            "-v",
            help=f"stream vibe [{', '.join(storage.VIBES)}]",
            prompt=f"💜 vibe [{'/'.join(storage.VIBES)}]",
        ),
    ] = "chill",
    notes: Annotated[
        str,
        typer.Option("--notes", "-n", help="any notes about the stream", prompt="📝 notes (optional, press enter to skip)"),
    ] = "",
    date: Annotated[
        Optional[str],
        typer.Option("--date", help="date in YYYY-MM-DD format (defaults to today)"),
    ] = None,
) -> None:
    """[bold]Log a new stream session.[/bold] Prompts for info if flags aren't given."""
    display.banner()

    if vibe not in storage.VIBES:
        display.print_error(f"vibe must be one of: {', '.join(storage.VIBES)}")
        raise typer.Exit(1)

    session = storage.add_session(
        game=game,
        duration_min=duration,
        peak_viewers=peak,
        avg_viewers=avg,
        clips=clips,
        new_followers=followers,
        vibe=vibe,
        notes=notes,
        date=date,
    )

    display.print_success(f"session saved! [dim](id: {session['id']})[/dim]")
    display.print_session_card(session)


@app.command()
def stats() -> None:
    """[bold]Show overall stats[/bold] across all your sessions."""
    display.banner()
    sessions = storage.load_sessions()
    s = storage.get_stats(sessions)
    display.print_stats(s, sessions)


@app.command()
def recent(
    n: Annotated[int, typer.Option("--n", help="number of sessions to show")] = 5
) -> None:
    """[bold]Show your most recent stream sessions.[/bold]"""
    display.banner()
    sessions = storage.load_sessions()
    display.print_recent(sessions, n=n)


@app.command()
def history(
    game: Annotated[
        Optional[str],
        typer.Option("--game", "-g", help="filter by game name (partial match)"),
    ] = None,
    vibe: Annotated[
        Optional[str],
        typer.Option("--vibe", "-v", help="filter by vibe"),
    ] = None,
    limit: Annotated[
        int,
        typer.Option("--limit", "-l", help="max sessions to show"),
    ] = 20,
) -> None:
    """[bold]Browse all sessions,[/bold] with optional filters."""
    display.banner()
    sessions = storage.load_sessions()

    if game:
        sessions = [s for s in sessions if game.lower() in s["game"].lower()]
    if vibe:
        sessions = [s for s in sessions if s["vibe"] == vibe]

    sessions = sorted(sessions, key=lambda s: s["date"], reverse=True)[:limit]

    if not sessions:
        display.print_error("no sessions match that filter")
        raise typer.Exit(1)

    display.console.print(
        f"\n[bold #9146FF]◈ session history[/bold #9146FF]"
        + (f" · game=[bold]{game}[/bold]" if game else "")
        + (f" · vibe=[bold]{vibe}[/bold]" if vibe else "")
        + f" · {len(sessions)} result(s)\n"
    )
    for i, s in enumerate(sessions, 1):
        display.print_session_card(s, index=i)


@app.command()
def delete(
    session_id: Annotated[str, typer.Argument(help="session ID to delete (shown in brackets in session cards)")],
) -> None:
    """[bold]Delete a session[/bold] by its ID."""
    ok = storage.delete_session(session_id)
    if ok:
        display.print_success(f"deleted session {session_id}")
    else:
        display.print_error(f"no session found with id '{session_id}'")
        raise typer.Exit(1)


@app.command()
def games() -> None:
    """[bold]List all games[/bold] you've streamed, sorted by hours."""
    display.banner()
    sessions = storage.load_sessions()
    s = storage.get_stats(sessions)
    if not s:
        display.print_error("no sessions yet!")
        raise typer.Exit(1)
    display.console.print(f"\n[bold #FF6AC9]◈ games streamed[/bold #FF6AC9]\n")
    for game, hours in sorted(s["game_hours"].items(), key=lambda x: -x[1]):
        count = s["game_counts"][game]
        bar = "█" * max(1, int(hours * 2))
        display.console.print(
            f"  [bold #F0E6FF]{game:<28}[/bold #F0E6FF]"
            f"[#9146FF]{bar}[/#9146FF]"
            f"  [dim]{hours:.1f}h  ·  {count} session{'s' if count != 1 else ''}[/dim]"
        )


def main() -> None:
    app()
