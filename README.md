# cali

`cali` is a small terminal-based calisthenics workout timer designed for morning workouts, Termux, tmux, and simple command-line use.

It detects the current day of the week, loads the matching workout, runs timed exercise/rest intervals, and plays a local WAV sound alert through `mpv`.

The project is intentionally lightweight:

- No Python runtime dependencies
- Works well inside `tmux`
- Designed for Termux on Android
- Includes a script to generate the `beep.wav` alert sound
- Supports pause, skip, and quit controls during workouts

## Project Layout

```text
.
├── main.py
├── Makefile
├── pyproject.toml
├── README.md
├── scripts
│   ├── beep_gen.py
│   └── workout.py
└── uv.lock
```

## Requirements

### Python

This project requires Python 3.11 or newer.

If using `uv`:

```bash
uv python install 3.11
uv sync
```

### Audio Playback

For sound alerts, install `mpv`.

On Termux:

```bash
pkg update
pkg install mpv
```

On Debian/Ubuntu:

```bash
sudo apt update
sudo apt install mpv
```

The workout script expects a sound file at:

```text
~/beep.wav
```

You can generate this file using the included beep generator script.

## Setup

Clone the repository:

```bash
git clone https://github.com/sethbarrett50/cali.git
cd cali
```

Sync the project with `uv`:

```bash
uv sync
```

Generate the alert sound:

```bash
uv run python scripts/beep_gen.py
```

This should create:

```text
~/beep.wav
```

Test the sound manually:

```bash
mpv --no-video --really-quiet ~/beep.wav
```

If you hear the sound, the workout timer should be able to use it.

## Running the Workout Timer

Run the main workout script:

```bash
uv run python scripts/workout.py
```

Or, if you are not using `uv`:

```bash
python scripts/workout.py
```

If you are using Termux/tmux, you can run:

```bash
tmux new -s workout
uv run python scripts/workout.py
```

## Controls

During a timer:

```text
p = pause/resume
s = skip current exercise or rest
q = quit
```

## Weekly Workout Schedule

The current schedule is:

```text
Monday    - Full Body Strength C
Tuesday   - Mobility + Core
Wednesday - Full Body Strength B
Thursday  - Conditioning Day
Friday    - Full Body Strength A
Saturday  - Longer Easy Session
Sunday    - Recovery / Reset
```

Each workout includes a warm-up, the main workout, rest timers, and a cooldown.

## Sound Alerts

Sound alerts use:

```bash
mpv --no-video --really-quiet ~/beep.wav
```

The project does not rely on Termux notifications, vibration, or text-to-speech because those can be inconsistent across Android devices and Termux installations.

If `~/beep.wav` is missing or `mpv` is not installed, the script falls back to a terminal bell. The terminal bell may be silent in some terminals.

## Generating the Beep Sound

The repository includes:

```text
scripts/beep_gen.py
```

Run:

```bash
uv run python scripts/beep_gen.py
```

This generates a short WAV alert at:

```text
~/beep.wav
```

You can adjust the beep generator script if you want to change the sound duration, frequency, or volume.

## Development

Install development tools:

```bash
uv sync --group dev
```

Run Ruff linting:

```bash
uv run ruff check .
```

Run Ruff formatting:

```bash
uv run ruff format .
```

Run deptry:

```bash
uv run deptry .
```

## Termux Notes

Recommended Termux setup:

```bash
pkg update
pkg install python uv mpv tmux
```

Then:

```bash
git clone https://github.com/sethbarrett50/cali.git
cd cali
uv sync
uv run python scripts/beep_gen.py
uv run python scripts/workout.py
```

To keep the workout running in a persistent terminal session:

```bash
tmux new -s workout
uv run python scripts/workout.py
```

Detach from tmux:

```text
Ctrl-b d
```

Reattach later:

```bash
tmux attach -t workout
```
