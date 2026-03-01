import sys

from zeptomc.cli import zeptomc_cli

MINPYVERSION = (3, 7, 0)

if sys.version_info < MINPYVERSION:
    print(
        "picomc requires at least Python version "
        "{}.{}.{}. You are using {}.{}.{}.".format(*MINPYVERSION, *sys.version_info)
    )
    sys.exit(1)


def main():
    zeptomc_cli()
