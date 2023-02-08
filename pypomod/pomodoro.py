#!/usr/bin/env python3
"""Pomodoro timer"""
import time
from collections.abc import Iterable
from datetime import datetime
from itertools import cycle

from pypomod import __version__
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
POMODORO_COLOR_GRAD_INV = ANSI.color_gradient(
    [255, 99, 71], [71, 227, 255], BAR_LENGTH
)
"""Progress bar color gradient. From light blue to tomato."""


def banner() -> None:
    """Prints the pypomod banner."""

    color_tomato = ANSI.rgb_to_ansi(255, 99, 71)

    banner_text = f"""
 ██▓███   ▒█████   ███▄ ▄███▓ ▒█████  ▓█████▄  ▒█████   ██▀███   ▒█████
 ▓██░  ██▒▒██▒  ██▒▓██▒▀█▀ ██▒▒██▒  ██▒▒██▀ ██▌▒██▒  ██▒▓██ ▒ ██▒▒██▒  ██▒
 ▓██░ ██▓▒▒██░  ██▒▓██    ▓██░▒██░  ██▒░██   █▌▒██░  ██▒▓██ ░▄█ ▒▒██░  ██▒
 ▒██▄█▓▒ ▒▒██   ██░▒██    ▒██ ▒██   ██░░▓█▄   ▌▒██   ██░▒██▀▀█▄  ▒██   ██░
 ▒██▒ ░  ░░ ████▓▒░▒██▒   ░██▒░ ████▓▒░░▒████▓ ░ ████▓▒░░██▓ ▒██▒░ ████▓▒░
 ▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒░   ░  ░░ ▒░▒░▒░  ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░ ▒░▒░▒░
 ░▒ ░       ░ ▒ ▒░ ░  ░      ░  ░ ▒ ▒░  ░ ▒  ▒   ░ ▒ ▒░   ░▒ ░ ▒░  ░ ▒ ▒░
 ░░       ░ ░ ░ ▒  ░      ░   ░ ░ ░ ▒   ░ ░  ░ ░ ░ ░ ▒    ░░   ░ ░ ░ ░ ▒
             ░ ░         ░       ░ ░     ░        ░ ░     ░         ░ ░
                                     ░
 v{__version__}
    """

    print(f"{color_tomato}{banner_text}{ANSI.END}")


def pomodoro(work_time: int, break_time: int, repeat: int) -> None:
    """Pomodoro timer.

    Args:
        work_time (int): Time in minutes for work.
        break_time (int): Time in minutes for break.
        repeat (int): Number of repeats.
    """

    work_now = True
    break_now = False

    banner()

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
            progress(break_time * 60, grad_inv=True)
            clear_line(1)
            Notification.notify("Pomodoro", "Time to work!")
            time.sleep(0.2)
            break_now = False
            work_now = True

    print(f"{Emoji.CHECK} {ANSI.GREEN}Well done!{ANSI.END} ")


def progress(time_target: int, grad_inv: bool = False) -> None:
    """Progress tracker

    Args:
        time_target (int): Target time in seconds.
        grad_inv (bool, optional): Use inverted color gradient. Defaults to False.
    """

    itr: int = 0
    finished: bool = False

    second_per_bar = int(round(time_target / float(BAR_LENGTH), 1))
    second_per_step = second_per_bar / len(BARS)

    gradient = "|"

    tri_emoji = next(Emoji.TRIATHLON)

    target_tic = time.perf_counter()
    tic = time.perf_counter()

    if grad_inv is False:
        color_grad = POMODORO_COLOR_GRAD
    else:
        color_grad = POMODORO_COLOR_GRAD_INV

    while finished is False:

        percentage = int(round(100.0 * itr / float(BAR_LENGTH - 1), 1))

        toc = time.perf_counter()
        transition = ""
        bar_adj = 1

        if toc - tic >= second_per_step:

            mins, secs = divmod(
                abs(time_target - (time.perf_counter() - target_tic)), 60
            )
            remaining_time = f"{int(mins):02d}m{int(secs):02d}s"
            current_time = datetime.now().strftime("%H:%M")
            time_display = f"{current_time} - {remaining_time} {tri_emoji}"

            bar_el = next(BAR_ITR)
            transition = f"{color_grad[itr]}{bar_el}{ANSI.END}"
            bar = (
                f"{time_display}\n\r{gradient + transition}"
                + CDOT * (BAR_LENGTH - itr - bar_adj)
                + "|"
            )
            print(bar + f" {percentage:01d} % done! ", end="\r")
            clear_line(1)

            # Update new time check
            tic = time.perf_counter()

            if bar_el == "█":
                tri_emoji = next(Emoji.TRIATHLON)
                gradient += transition
                itr += 1

        if percentage > 100:
            finished = True
