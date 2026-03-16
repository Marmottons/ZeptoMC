import click

from zeptomc import mod


@click.group()
def install_cli():
    """Install a mod loader (Forge or Fabric).

    Available loaders:

    \b
      forge   Forge loader (https://minecraftforge.net)
      fabric  Fabric loader (https://fabricmc.net)

    VERSION is optional. If omitted, the latest stable version is installed.

    \b
    Examples:
      zeptomc install forge 1.8.9
      zeptomc install forge
      zeptomc install fabric 1.20.1
      zeptomc install fabric"""
    pass


for loader in mod.LOADERS:
    loader.register_cli(install_cli)


def register_install_cli(zeptomc_cli):
    zeptomc_cli.add_command(install_cli, name="install")
