"""Colored console output (no emojis)."""

import sys


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"


# If stdout is not a real terminal (redirected to a file, for example),
# colors are turned off so the text doesn't get messy with ANSI codes.
_COLOR_ENABLED = sys.stdout.isatty()


def _paint(color: str, label: str, message: str) -> str:
    if not _COLOR_ENABLED:
        return f"[{label}] {message}"
    return f"{color}[{label}]{Colors.RESET} {message}"


def info(message: str):
    print(_paint(Colors.CYAN, "INFO", message))


def success(message: str):
    print(_paint(Colors.GREEN, "OK", message))


def warning(message: str):
    print(_paint(Colors.YELLOW, "WARN", message))


def error(message: str):
    print(_paint(Colors.RED, "ERROR", message))


def title(message: str):
    if not _COLOR_ENABLED:
        print(message)
        return
    print(f"{Colors.BOLD}{Colors.CYAN}{message}{Colors.RESET}")
