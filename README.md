# streamlog

A command-line tool for Twitch streamers to log and track stream sessions right from the terminal. Record your game, viewer counts, clips, new followers, and the general vibe of each stream — then pull up stats and trends whenever you want without opening a spreadsheet.

## Installation

```bash
uv add "git+https://github.com/havuong/streamlog.git"
```

Or clone and install locally:

```bash
git clone https://github.com/havuong/streamlog.git
cd streamlog
uv sync
uv run streamlog --help
```

## Usage

### Log a session

Run interactively (recommended after streaming):

```bash
streamlog log
```

Or pass everything as flags for quick logging:

```bash
streamlog log --game "League of Legends" --duration 180 --peak 55 --avg 38 --clips 4 --followers 6 --vibe hype --notes "hit plat finally!!"
```

Available vibes: `cozy`, `hype`, `tilted`, `chill`, `grind`, `chaotic`, `goated`

### View your stats

```bash
streamlog stats
```

Shows total sessions, hours streamed, clips made, followers gained, average viewer counts, your best stream ever, a game breakdown, and vibe distribution.

### See recent sessions

```bash
streamlog recent          # last 5 streams
streamlog recent --n 10   # last 10
```

### Browse history with filters

```bash
streamlog history
streamlog history --game "Marvel Rivals"
streamlog history --vibe hype
streamlog history --game league --limit 5
```

### Games breakdown

```bash
streamlog games
```

Shows every game you've streamed with hours and session count, sorted by time streamed.

### Delete a session

```bash
streamlog delete abc12345   # use the ID shown in brackets on session cards
```

## Data

Sessions are stored locally at `~/.streamlog/sessions.json`. No accounts, no internet required.
