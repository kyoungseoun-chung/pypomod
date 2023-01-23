#!/usr/bin/env python3
"""Pomodoro timer"""
import time
from collections.abc import Iterable
from datetime import datetime
from itertools import cycle

from pypomod.tools import ANSI
from pypomod.tools import clear_line
from pypomod.tools import Emoji
from pypomod.tools import Notification

BARS: str = "▏▎▍▌▋▊▉█"
BAR_ITR: Iterable[str] = cycle(BARS)
"""Bar characters for smooth transition."""
CDOT: str = "·"
"""Center dot character for progress bar."""
BAR_LENGTH: int = 60
"""Fixed progress bar width."""
POMODORO_COLOR_GRAD = ANSI.color_gradient(
    [71, 227, 255], [255, 99, 71], BAR_LENGTH
)
"""Progress bar color gradient. From light blue to tomato."""


def banner() -> None:
    """Prints the pypomod banner."""
    pass


def pomodoro(work_time: int, break_time: int, repeat: int) -> None:
    """Pomodoro timer.

    Args:
        work_time (int): Time in minutes for work.
        break_time (int): Time in minutes for break.
        repeat (int): Number of repeats.
    """

    work_now: bool = True
    break_now: bool = False

    for i in range(repeat):

        if work_now:
            print(
                f"{i+1}/{repeat}: {ANSI.RED}Work hard!{ANSI.END} {Emoji.FIRE}",
            )
            progress(work_time * 60)
            clear_line(1)
            Notification.notify("Pomodoro", "Time to take a break!")
            work_now = False
            break_now = True

        if break_now:
            print(
                f"{i+1}/{repeat}: {ANSI.BLUE}Now take a break!{ANSI.END} {Emoji.WIND}",
            )
            progress(break_time * 60)
            clear_line(1)
            Notification.notify("Pomodoro", "Time to work!")
            time.sleep(0.2)
            break_now = False
            work_now = True


def progress(time_remain: int) -> None:
    """Progress tracker.

    Layout:
        Current time | Remaining time
        Progress bar | Percentage
    """
    time_sec = time_remain

    gradient = "|"

    for t in range(BAR_LENGTH):

        percentage = int(round(100.0 * t / float(BAR_LENGTH - 1), 1))

        second_per_bar = int(round(time_remain / float(BAR_LENGTH), 1))
        second_per_step = second_per_bar / len(BARS)

        tic = time.perf_counter()

        transition = ""

        tri_emoji = next(Emoji.TRIATHLON)
        for b in BARS:

            mins, secs = divmod(time_sec, 60)
            remaining_time = f"{int(mins):02d}m{int(secs):02d}s"
            current_time = datetime.now().strftime("%H:%M:%S")
            time_display = f"{current_time} - {remaining_time} {tri_emoji}"

            transition = f"{POMODORO_COLOR_GRAD[t]}{b}{ANSI.END}"
            bar = (
                f"{time_display}\n\r{gradient + transition}"
                + CDOT * (BAR_LENGTH - t - 1)
                + "|"
            )
            print(bar + f" {percentage:01d} %  ", end="\r")
            clear_line(1)
            time.sleep(second_per_step)

            toc = time.perf_counter()

            if time.perf_counter() - tic >= 1:
                time_sec -= toc - tic
                tic = time.perf_counter()

        gradient += transition
