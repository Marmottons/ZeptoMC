import os
from functools import partial
from pathlib import Path

import click

from zeptomc import logging
from zeptomc.launcher import Launcher
from zeptomc.logging import logger


class OrderedGroup(click.Group):
    def __init__(self, *args, **kwargs):
        self._cmd_order = []
        super().__init__(*args, **kwargs)

    def add_command(self, cmd, name=None):
        super().add_command(cmd, name)
        self._cmd_order.append(name or cmd.name)

    def list_commands(self, ctx):
        return self._cmd_order


def print_version(printer):
    import importlib.metadata
    import platform

    try:
        version = importlib.metadata.version("zeptomc")
    except importlib.metadata.PackageNotFoundError:
        version = "?"

    printer("zeptomc, version {}".format(version))
    printer("Python {}".format(platform.python_version()))


@click.group(cls=OrderedGroup, context_settings=dict(help_option_names=["--help", "--h"]))
@click.option("--debug", is_flag=True, default=False, help="Enable debug mode with detailed logs")
@click.option("-r", "--root", help="Custom data directory (default: ~/.zeptomc)", default=None)
@click.pass_context
def zeptomc_cli(ctx: click.Context, debug, root):
    """Launch Minecraft from the CLI."""
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
