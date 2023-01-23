#!/usr/bin/env python3
import time

from pypomod.tools import ANSI
from pypomod.tools import clear_line


def test_colors() -> None:
    smooth = "▏▎▍▌▋▊▉█"
    blank = "░"

    color_grad = ANSI.color_gradient([0, 0, 255], [255, 0, 0], 10)

    gradient = ""
    for c in color_grad:
        for s in smooth:
            gradient += f"{c}{s}{ANSI.END}"

    print(gradient)

    color_grad = ANSI.color_gradient([71, 227, 255], [255, 99, 71], 50)

    gradient = "| "
    for idx, c in enumerate(color_grad):
        transition = ""
        for s in smooth:
            transition = f"{c}{s}{ANSI.END}"
            print(
                f"{idx}-test\n\r{gradient + transition}"
                + "·" * (50 - idx - 1)
                + "|",
                end="\r",
            )
            clear_line(1)
            time.sleep(0.1 / len(smooth))
        gradient += transition


if __name__ == "__main__":
    test_colors()
