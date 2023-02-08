#!/usr/bin/env python3
import argparse

from pypomod.pomodoro import pomodoro
from pypomod.tools import clear_terminal

parser = argparse.ArgumentParser(
    prog="pympod",
    description="A simple python CLI package for the pomodoro timer.",
)
parser.add_argument(
    "-w",
    "--work_time",
    help="Set the work time. Default is 20 minutes.",
    default=20,
    type=int,
)
parser.add_argument(
    "-b",
    "--break_time",
    help="Set the break time. Default is 5 minutes.",
    default=5,
    type=int,
)
parser.add_argument(
    "-r",
    "--repeat",
    help="Set the number of repeats. Default is 1.",
    default=1,
    type=int,
)


def main():

    args = parser.parse_args()
    clear_terminal()
    pomodoro(args.work_time, args.break_time, args.repeat)


if __name__ == "__main__":
    """Make the main function can be called when the script is run directly."""
    main()
