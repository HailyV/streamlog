"""Rich display components for streamlog - cute purple/pink Twitch aesthetic."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.align import Align
from rich import box
from rich.style import Style

console = Console()

# Twitch palette
PURPLE = "#9146FF"
PINK = "#FF6AC9"
TEAL = "#00D4AA"
GOLD = "#FFD700"
SOFT_WHITE = "#F0E6FF"
DIM = "#9E8FBB"

VIBE_EMOJI = {
    "cozy": "☕",
    "hype": "🔥",
    "tilted": "😤",
    "chill": "🌊",
    "grind": "⚔️",
    "chaotic": "🌀",
    "goated": "🐐",
}

VIBE_COLOR = {
    "cozy": "#FFB347",
    "hype": "#FF4444",
    "tilted": "#FF6B35",
    "chill": "#4FC3F7",
    "grind": "#AB47BC",
    "chaotic": "#FF80AB",
    "goated": GOLD,
}


def vibe_badge(vibe: str) -> Text:
    emoji = VIBE_EMOJI.get(vibe, "✨")
    color = VIBE_COLOR.get(vibe, SOFT_WHITE)
    t = Text()
    t.append(f" {emoji} {vibe} ", style=f"bold {color}")
    return t


def banner() -> None:
    art = Text(justify="center")
    art.append("  ◈ ", style=f"bold {PURPLE}")
    art.append("streamlog", style=f"bold {PINK}")
    art.append(" ◈  ", style=f"bold {PURPLE}")
    art.append("your twitch session tracker", style=f"italic {DIM}")
    console.print(Panel(art, border_style=PURPLE, padding=(0, 2)))


def print_session_card(session: dict, index: int | None = None) -> None:
    vibe = session.get("vibe", "chill")
    vbadge = vibe_badge(vibe)

    title = Text()
    if index is not None:
        title.append(f"#{index}  ", style=f"dim {DIM}")
    title.append(f"[{session['id']}]  ", style=f"dim {DIM}")
    title.append(session["date"], style=f"bold {SOFT_WHITE}")
    title.append("  —  ", style=f"{DIM}")
    title.append(session["game"], style=f"bold {PINK}")

    body = Table.grid(padding=(0, 2))
    body.add_column(style=f"dim {DIM}")
    body.add_column(style=f"bold {SOFT_WHITE}")

    dur = session["duration_min"]
    body.add_row("⏱  duration", f"{dur // 60}h {dur % 60}m")
    body.add_row("👀 peak viewers", str(session["peak_viewers"]))
    body.add_row("📊 avg viewers", str(session["avg_viewers"]))
    body.add_row("✂️  clips made", str(session["clips"]))
    body.add_row("➕ new followers", str(session["new_followers"]))

    row2 = Table.grid(padding=(0, 2))
    row2.add_column(style=f"dim {DIM}")
    row2.add_column()
    row2.add_row("vibe", vbadge)
    if session.get("notes"):
        row2.add_row("notes", Text(session["notes"], style=f"italic {DIM}"))

    inner = Table.grid()
    inner.add_column()
    inner.add_row(body)
    inner.add_row(row2)

    console.print(Panel(inner, title=title, border_style=PURPLE, padding=(0, 1)))


def print_stats(stats: dict, sessions: list[dict]) -> None:
    if not stats:
        console.print(Panel(
            Text("no sessions logged yet! run [bold]streamlog log[/bold] to start", justify="center"),
            border_style=PURPLE
        ))
        return

    # Hero numbers row
    def big_stat(value: str, label: str, color: str) -> Panel:
        t = Text(justify="center")
        t.append(f"\n{value}\n", style=f"bold {color}")
        t.append(label, style=f"dim {DIM}")
        t.append("\n")
        return Panel(t, border_style=color, padding=(0, 1))

    hero = Columns([
        big_stat(str(stats["total_sessions"]), "sessions", PURPLE),
        big_stat(f"{stats['total_hours']}h", "streamed", PINK),
        big_stat(str(stats["total_clips"]), "clips", TEAL),
        big_stat(f"+{stats['total_followers']}", "followers", GOLD),
    ], equal=True)
    console.print(hero)

    # Viewer stats
    viewer_tbl = Table(box=box.SIMPLE_HEAVY, border_style=PURPLE, padding=(0, 2))
    viewer_tbl.add_column("metric", style=f"dim {DIM}")
    viewer_tbl.add_column("value", style=f"bold {SOFT_WHITE}", justify="right")
    viewer_tbl.add_row("avg peak viewers", f"{stats['avg_peak_viewers']}")
    viewer_tbl.add_row("avg avg viewers", f"{stats['avg_avg_viewers']}")
    best = stats["best_session"]
    viewer_tbl.add_row(
        "best stream",
        f"{best['date']} · {best['game']} · {best['peak_viewers']} peak",
    )
    console.print(Panel(viewer_tbl, title=Text(" 📺 viewers ", style=f"bold {PINK}"), border_style=PURPLE))

    # Game breakdown
    game_tbl = Table(box=box.SIMPLE_HEAVY, border_style=PURPLE, padding=(0, 2))
    game_tbl.add_column("game", style=f"bold {SOFT_WHITE}")
    game_tbl.add_column("sessions", justify="right", style=f"{TEAL}")
    game_tbl.add_column("hours", justify="right", style=f"{PINK}")
    for game, count in sorted(stats["game_counts"].items(), key=lambda x: -x[1]):
        hours = stats["game_hours"].get(game, 0)
        game_tbl.add_row(game, str(count), f"{hours:.1f}h")
    console.print(Panel(game_tbl, title=Text(" 🎮 games ", style=f"bold {PINK}"), border_style=PURPLE))

    # Vibe breakdown
    vibe_tbl = Table(box=box.SIMPLE, border_style=PURPLE, padding=(0, 2))
    vibe_tbl.add_column("vibe")
    vibe_tbl.add_column("count", justify="right", style=f"{SOFT_WHITE}")
    for vibe, count in sorted(stats["vibe_counts"].items(), key=lambda x: -x[1]):
        emoji = VIBE_EMOJI.get(vibe, "✨")
        color = VIBE_COLOR.get(vibe, SOFT_WHITE)
        vibe_tbl.add_row(Text(f"{emoji} {vibe}", style=f"bold {color}"), str(count))
    console.print(Panel(vibe_tbl, title=Text(" 💜 vibes ", style=f"bold {PINK}"), border_style=PURPLE))


def print_recent(sessions: list[dict], n: int = 5) -> None:
    recent = sorted(sessions, key=lambda s: s["date"], reverse=True)[:n]
    if not recent:
        console.print(Panel(
            Text("no sessions yet! use [bold]streamlog log[/bold] to add one", justify="center"),
            border_style=PURPLE,
        ))
        return
    console.print(f"\n[bold {PINK}]◈ recent streams[/bold {PINK}]\n")
    for i, s in enumerate(recent, 1):
        print_session_card(s, index=i)


def print_success(msg: str) -> None:
    console.print(f"[bold {TEAL}]✓[/bold {TEAL}]  {msg}")


def print_error(msg: str) -> None:
    console.print(f"[bold red]✗[/bold red]  {msg}")
