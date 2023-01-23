#!/usr/bin/env python3
"""Collection of useful tools for pypomod."""
import platform
import subprocess
from itertools import cycle


class ANSI:
    """Collection of ANSI color codes.

    Can be used like

        >>> print(f"{Colors.RED}Hello{Colors.END}")
    """

    RED: str = "\033[31m"
    GREEN: str = "\033[32m"
    YELLOW: str = "\033[33m"
    BLUE: str = "\033[34m"
    MAGENTA: str = "\033[35m"
    CYAN: str = "\033[36m"
    UNDERLINE: str = "\033[4m"
    END: str = "\033[0m"
    LINECLEAR: str = "\033[2K"
    LINEUP: str = "\033[1A"

    @staticmethod
    def rgb_to_ansi(r: int, g: int, b: int) -> str:
        """Convert RGB to ANSI color code."""
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def color_gradient(
        begin: list[int], end: list[int], steps: int
    ) -> list[str]:
        """Create a gradient of ANSI color codes.

        Args:
            begin (list[int]): RGB color code for the beginning.
            end (list[int]): RGB color code for the end.
            steps (int): Number of steps.

        Returns:
            list[str]: List of ANSI color codes.
        """
        r1, g1, b1 = begin
        r2, g2, b2 = end

        r_step = (r2 - r1) / steps
        g_step = (g2 - g1) / steps
        b_step = (b2 - b1) / steps

        return [
            ANSI.rgb_to_ansi(
                int(r1 + r_step * i),
                int(g1 + g_step * i),
                int(b1 + b_step * i),
            )
            for i in range(steps)
        ]


class Emoji:
    """Collection of emoji unicodes."""

    FIRE: str = "🔥"
    WIND: str = "🏖️"
    TRIATHLON = cycle(["🏊", "🚴", "🏃"])


class Notification:
    @staticmethod
    def notify(title: str, message: str) -> None:
        """Send a notification to the OSX notification center."""

        if platform.system() == "Darwin":

            subprocess.run(["afplay", "/System/Library/Sounds/Submarine.aiff"])
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    f'display notification "{message}" with title "{title}"',
                ]
            )
        elif platform.system() == "Linux":
            # TODO: test Linux later and also add ring tone support
            subprocess.run(["notify-send", title, message])
        else:
            raise NotImplementedError("Window is not supported yet.")


def clear_terminal() -> None:
    """Clear the terminal."""
    subprocess.run(["clear"])


def clear_line(n_lines: int) -> None:
    """Clear `n_lines` in the terminal."""
    for _ in range(n_lines):
        print(ANSI.LINEUP, end=ANSI.LINECLEAR)
