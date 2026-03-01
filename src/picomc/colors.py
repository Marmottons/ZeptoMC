"""ANSI color codes for terminal output (no external dependencies)"""

import logging

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BRIGHT = "\033[1m"
NORMAL = "\033[0m"
RESET = "\033[0m"

# Log level colors
LOG_COLORS = {
    "DEBUG": CYAN,
    "INFO": GREEN,
    "WARNING": YELLOW,
    "ERROR": RED,
    "CRITICAL": f"{RED}{BRIGHT}",
}


class ColorFormatter(logging.Formatter):
    """Custom logging formatter with ANSI colors"""

    def format(self, record):
        levelname = record.levelname
        color = LOG_COLORS.get(levelname, NORMAL)
        record.levelname = f"{color}{levelname}{RESET}"
        return super().format(record)


def colorize(text, color):
    """Add ANSI color to text"""
    return f"{color}{text}{RESET}"
