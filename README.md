# Focus Timer

A Pomodoro-style focus timer in two flavors: a browser app and a terminal app.

## Browser (`index.html`)

Open `index.html` directly in any browser — no server needed.

- Animated ring counts down each phase
- Work → Short Break → Work → … → Long Break (every 4 sessions)
- Desktop notifications and a soft audio beep when a phase ends
- Session count persisted in `localStorage`

## Terminal (`timer.py`)

Requires Python 3. No dependencies.

```bash
python3 timer.py
```

- Color progress bar in your terminal
- Press **Enter** to start each phase, **Ctrl+C** to skip, **Ctrl+C** again at the prompt to quit
- Session count saved to `.timer_state.json` in the same folder

## Defaults

| Phase       | Duration |
|-------------|----------|
| Work        | 25 min   |
| Short break | 5 min    |
| Long break  | 15 min   |

Long break triggers every 4 completed work sessions. Edit the constants at the top of either file to change durations.
