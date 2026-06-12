"""Storage layer for streamlog - reads/writes JSON to ~/.streamlog/sessions.json"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

STREAMLOG_DIR = Path.home() / ".streamlog"
SESSIONS_FILE = STREAMLOG_DIR / "sessions.json"

VIBES = ["cozy", "hype", "tilted", "chill", "grind", "chaotic", "goated"]
GAMES_AUTOCOMPLETE = [
    "League of Legends",
    "Marvel Rivals",
    "Valorant",
    "Minecraft",
    "Stardew Valley",
    "Elden Ring",
    "Just Chatting",
    "Creative",
]


def ensure_dir() -> None:
    STREAMLOG_DIR.mkdir(parents=True, exist_ok=True)


def load_sessions() -> list[dict]:
    ensure_dir()
    if not SESSIONS_FILE.exists():
        return []
    with open(SESSIONS_FILE) as f:
        return json.load(f)


def save_sessions(sessions: list[dict]) -> None:
    ensure_dir()
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f, indent=2, default=str)


def add_session(
    game: str,
    duration_min: int,
    peak_viewers: int,
    avg_viewers: int,
    clips: int,
    new_followers: int,
    vibe: str,
    notes: str,
    date: Optional[str] = None,
) -> dict:
    sessions = load_sessions()
    session = {
        "id": str(uuid.uuid4())[:8],
        "date": date or datetime.now().strftime("%Y-%m-%d"),
        "game": game,
        "duration_min": duration_min,
        "peak_viewers": peak_viewers,
        "avg_viewers": avg_viewers,
        "clips": clips,
        "new_followers": new_followers,
        "vibe": vibe,
        "notes": notes,
        "logged_at": datetime.now().isoformat(),
    }
    sessions.append(session)
    save_sessions(sessions)
    return session


def delete_session(session_id: str) -> bool:
    sessions = load_sessions()
    before = len(sessions)
    sessions = [s for s in sessions if s["id"] != session_id]
    if len(sessions) == before:
        return False
    save_sessions(sessions)
    return True


def get_stats(sessions: list[dict]) -> dict:
    if not sessions:
        return {}
    total_hours = sum(s["duration_min"] for s in sessions) / 60
    total_clips = sum(s["clips"] for s in sessions)
    total_followers = sum(s["new_followers"] for s in sessions)
    avg_peak = sum(s["peak_viewers"] for s in sessions) / len(sessions)
    avg_avg = sum(s["avg_viewers"] for s in sessions) / len(sessions)
    best = max(sessions, key=lambda s: s["peak_viewers"])

    # game breakdown
    game_counts: dict[str, int] = {}
    game_hours: dict[str, float] = {}
    for s in sessions:
        g = s["game"]
        game_counts[g] = game_counts.get(g, 0) + 1
        game_hours[g] = game_hours.get(g, 0) + s["duration_min"] / 60

    # vibe breakdown
    vibe_counts: dict[str, int] = {}
    for s in sessions:
        v = s["vibe"]
        vibe_counts[v] = vibe_counts.get(v, 0) + 1

    return {
        "total_sessions": len(sessions),
        "total_hours": round(total_hours, 1),
        "total_clips": total_clips,
        "total_followers": total_followers,
        "avg_peak_viewers": round(avg_peak, 1),
        "avg_avg_viewers": round(avg_avg, 1),
        "best_session": best,
        "game_counts": game_counts,
        "game_hours": game_hours,
        "vibe_counts": vibe_counts,
    }
