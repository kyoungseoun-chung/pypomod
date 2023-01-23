# Pypomod

A simple python CLI package for the pomodoro timer.

> Currently, only works on macOS

## Installation

```bash
pip install pypomod
```

## Use case

### Demo

![screenshot](./assets/screenshot.png)

### Options

```bash
pomodoro -h

usage: pympod [-h] [-w WORK_TIME] [-b BREAK_TIME] [-r REPEAT]

A simple python CLI package for the pomodoro timer.

options:
  -h, --help            show this help message and exit
  -w WORK_TIME, --work_time WORK_TIME
                        Set the work time. Default is 20 minutes.
  -b BREAK_TIME, --break_time BREAK_TIME
                        Set the break time. Default is 5 minutes.
  -r REPEAT, --repeat REPEAT
                        Set the number of repeats. Default is 1.
```

## Known issue

- [ ] Remaining time is not updated by a second.
- [ ] Linux and Windows are not fully supported yet.
