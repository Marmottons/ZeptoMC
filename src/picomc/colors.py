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


class ProgressBar:
    """Simple progress bar without external dependencies"""

    def __init__(self, total, disable=False, unit="", unit_scale=False, unit_divisor=1000):
        self.total = total
        self.current = 0
        self.disable = disable
        self.unit = unit
        self.unit_scale = unit_scale
        self.unit_divisor = unit_divisor

    def update(self, n=1):
        """Update progress by n items"""
        if not self.disable:
            self.current += n
            self._draw()

    def _format_size(self, size):
        """Format bytes to human-readable size"""
        if not self.unit_scale or not self.unit:
            return str(size)
        
        units = ["", "K", "M", "G"]
        divisor = self.unit_divisor
        size_f = float(size)
        
        for unit in units:
            if size_f < divisor:
                return f"{size_f:.1f}{unit}"
            size_f /= divisor
        
        return f"{size_f:.1f}T"

    def _draw(self):
        """Draw progress bar to stdout"""
        if self.total == 0:
            return
        
        percent = min(100, (self.current / self.total) * 100)
        bar_len = 30
        filled = int(bar_len * self.current / self.total)
        bar = "█" * filled + "░" * (bar_len - filled)
        
        current_str = self._format_size(self.current) if self.unit_scale else str(self.current)
        total_str = self._format_size(self.total) if self.unit_scale else str(self.total)
        
        info = f"{current_str}/{total_str}"
        if self.unit:
            info += self.unit
        
        print(f"\r[{bar}] {percent:.0f}% {info}", end="", flush=True)

    def close(self):
        """Close progress bar"""
        if not self.disable:
            print()  # New line at the end

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
