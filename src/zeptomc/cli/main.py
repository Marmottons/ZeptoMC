import os
from functools import partial
from pathlib import Path

import click

from zeptomc import logging
from zeptomc.launcher import Launcher
from zeptomc.logging import logger


def print_version(printer):
    import importlib.metadata
    import platform

    try:
        version = importlib.metadata.version("zeptomc")
    except importlib.metadata.PackageNotFoundError:
        version = "?"

    printer("zeptomc, version {}".format(version))
    printer("Python {}".format(platform.python_version()))


def click_print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    print_version(click.echo)
    ctx.exit()


@click.group()
@click.option("--debug/--no-debug", default=None, help="Enable debug mode with detailed logs")
@click.option("-r", "--root", help="Custom data directory (default: ~/.zeptomc)", default=None)
@click.option(
    "--version",
    is_flag=True,
    callback=click_print_version,
    expose_value=False,
    is_eager=True,
)
@click.pass_context
def zeptomc_cli(ctx: click.Context, debug, root):
    """A minimal, lightweight Minecraft launcher with no bloat.
    
    Quick start:
      zeptomc play
      zeptomc account create
      zeptomc instance list
    
    For more help: zeptomc COMMAND --help"""
    logging.initialize(debug)

    if debug:
        print_version(logger.debug)

    final_root = os.getenv("ZEPTOMC_ROOT")
    if root is not None:
        final_root = root

    if final_root is not None:
        final_root = Path(final_root).resolve()

    launcher_cm = Launcher.new(root=final_root, debug=debug)
    launcher = launcher_cm.__enter__()
    ctx.call_on_close(partial(launcher_cm.__exit__, None, None, None))

    ctx.obj = launcher
