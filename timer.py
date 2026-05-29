#!/usr/bin/env python3
import time
import sys
import os
import json
import signal
from datetime import datetime

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), ".timer_state.json")

WORK_MINS = 25
SHORT_BREAK_MINS = 5
LONG_BREAK_MINS = 15
SESSIONS_BEFORE_LONG = 4

COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "cyan": "\033[96m",
    "magenta": "\033[95m",
    "dim": "\033[2m",
}

def c(color, text):
    return f"{COLORS[color]}{text}{COLORS['reset']}"

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def load_state():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"sessions_today": 0, "last_date": "", "total_sessions": 0}

def save_state(state):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(state, f)

def progress_bar(elapsed, total, width=40):
    pct = elapsed / total
    filled = int(pct * width)
    bar = "█" * filled + "░" * (width - filled)
    return bar, pct

def fmt_time(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"

def bell():
    print("\a", end="", flush=True)

def run_phase(label, duration_mins, color, state):
    total = duration_mins * 60
    start = time.time()

    def handle_skip(sig, frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, handle_skip)

    try:
        while True:
            elapsed = time.time() - start
            remaining = total - elapsed
            if remaining <= 0:
                break

            bar, pct = progress_bar(elapsed, total)
            time_str = fmt_time(remaining)

            clear()
            print()
            print(c("bold", f"  🍅 Focus Timer"))
            print(c("dim", f"  Sessions today: {state['sessions_today']}  |  All time: {state['total_sessions']}"))
            print()
            print(c(color, c("bold", f"  {label}")))
            print()
            print(f"  {c(color, bar)}")
            print()
            print(c("bold", f"  {time_str} remaining") + c("dim", f"  ({int(pct*100)}%)"))
            print()
            print(c("dim", "  Press Ctrl+C to skip this phase"))

            time.sleep(0.5)

    except KeyboardInterrupt:
        clear()
        print()
        print(c("yellow", "  ⏭  Phase skipped."))
        time.sleep(1)
        return False

    bell()
    return True

def main():
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    if state["last_date"] != today:
        state["sessions_today"] = 0
        state["last_date"] = today

    session_num = 0

    clear()
    print()
    print(c("bold", "  🍅 Focus Timer — Pomodoro"))
    print()
    print(f"  {c('cyan', str(WORK_MINS))} min work  •  {c('green', str(SHORT_BREAK_MINS))} min break  •  {c('magenta', str(LONG_BREAK_MINS))} min long break every {SESSIONS_BEFORE_LONG} sessions")
    print()
    print(c("dim", "  Press Enter to start, Ctrl+C to quit"))
    print()

    try:
        input()
    except KeyboardInterrupt:
        print("\n  Bye!\n")
        return

    while True:
        session_num += 1
        label = f"Work Session #{session_num}"

        completed = run_phase(label, WORK_MINS, "red", state)
        if completed:
            state["sessions_today"] += 1
            state["total_sessions"] += 1
            save_state(state)

            clear()
            print()
            print(c("green", c("bold", f"  ✅ Session complete! Great work.")))
            print(c("dim", f"  Sessions today: {state['sessions_today']}  |  All time: {state['total_sessions']}"))
            print()

            if session_num % SESSIONS_BEFORE_LONG == 0:
                print(c("magenta", f"  🎉 Long break time! ({LONG_BREAK_MINS} min)"))
                print()
                print(c("dim", "  Press Enter to start break, Ctrl+C to quit"))
                try:
                    input()
                except KeyboardInterrupt:
                    break
                run_phase("Long Break", LONG_BREAK_MINS, "magenta", state)
            else:
                print(c("green", f"  ☕ Short break time! ({SHORT_BREAK_MINS} min)"))
                print()
                print(c("dim", "  Press Enter to start break, Ctrl+C to quit"))
                try:
                    input()
                except KeyboardInterrupt:
                    break
                run_phase("Short Break", SHORT_BREAK_MINS, "green", state)

        clear()
        print()
        print(c("cyan", "  Ready for the next session?"))
        print(c("dim",  "  Press Enter to start, Ctrl+C to quit"))
        print()
        try:
            input()
        except KeyboardInterrupt:
            break

    print()
    print(c("bold", f"  👋 Done for now! Sessions today: {state['sessions_today']}"))
    print()

if __name__ == "__main__":
    main()
