# cali-workout

`cali-workout` is a terminal-based calisthenics workout timer designed for morning workouts, Termux, tmux, and simple command-line use.

It detects the current day of the week, loads the matching workout, runs timed exercise/rest intervals, and plays a generated WAV sound alert through `mpv`.

## Features

- Terminal-based workout timer
- Day-of-week workout selection
- Warm-up, workout, rest, and cooldown timers
- Pause, skip, and quit controls
- Auto-generates `~/beep.wav` if missing
- Uses `mpv` for sound alerts when available
- Works well in Termux and tmux
- No Python runtime dependencies

## Installation

### Recommended: uvx

After the package is published to PyPI:

```bash
uvx cali-workout
````

You can also run the shorter alias:

```bash
uvx --from cali-workout cali
```

### Local development

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/cali-workout.git
cd cali-workout
```

Install/sync with `uv`:

```bash
uv sync --group dev
```

Run locally:

```bash
uv run cali-workout
```

Or:

```bash
uv run cali
```

## Termux Setup

Install the recommended system packages:

```bash
pkg update
pkg install python uv mpv tmux
```

Then run:

```bash
uvx cali-workout
```

For local development in Termux:

```bash
git clone https://github.com/YOUR_USERNAME/cali-workout.git
cd cali-workout
uv sync --group dev
uv run cali-workout
```

## Sound Alerts

`cali-workout` automatically creates:

```text
~/beep.wav
```

if it does not already exist.

Sound playback uses:

```bash
mpv --no-video --really-quiet ~/beep.wav
```

If `mpv` is not installed, the app falls back to a terminal bell. The terminal bell may be silent in Termux, so `mpv` is recommended.

To manually generate the beep file:

```bash
uv run cali-workout --generate-beep
```

To manually test the sound:

```bash
mpv --no-video --really-quiet ~/beep.wav
```

## Controls

During a timer:

```text
p = pause/resume
s = skip current exercise or rest
q = quit
```

## Weekly Schedule

```text
Monday    - Full Body Strength C
Tuesday   - Mobility + Core
Wednesday - Full Body Strength B
Thursday  - Conditioning Day
Friday    - Full Body Strength A
Saturday  - Longer Easy Session
Sunday    - Recovery / Reset
```

## Development Commands

Install development dependencies:

```bash
uv sync --group dev
```

Run the app:

```bash
uv run cali-workout
```

Lint:

```bash
uv run ruff check .
```

Format:

```bash
uv run ruff format .
```

Check dependencies:

```bash
uv run deptry .
```

Build:

```bash
uv build
```

Check distribution:

```bash
uv run twine check dist/*
```

Publish to PyPI:

```bash
uv publish
```

## Build and Test Package Locally

Build the package:

```bash
uv build
```

Test it with uvx from the local wheel:

```bash
uvx --from dist/cali_workout-0.1.0-py3-none-any.whl cali-workout
```

## License

MIT License.