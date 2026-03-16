import sys

from zeptomc.cli import zeptomc_cli

MINPYVERSION = (3, 8, 0)

if sys.version_info < MINPYVERSION:
    print(
        "zeptomc requires at least Python version "
        "{}.{}.{}. You are using {}.{}.{}.".format(*MINPYVERSION, *sys.version_info)
    )
    sys.exit(1)


def main():
    zeptomc_cli(prog_name="zeptomc")
