import click

from zeptomc import mod


@click.group()
def mod_cli():
    """Install and manage mod loaders.
    
    Mod loaders add support for mods and modpacks to Minecraft.
    Supported loaders: Forge, Fabric
    
    Examples:
      zeptomc mod loader list
      zeptomc mod loader forge 1.20.1
      zeptomc mod loader fabric 1.20"""
    pass


def list_loaders(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    for loader in mod.LOADERS:
        print(loader._loader_name)
    ctx.exit()


@mod_cli.group("loader")
@click.option(
    "--list",
    "-l",
    is_eager=True,
    is_flag=True,
    expose_value=False,
    callback=list_loaders,
    help="List available mod loaders",
)
def loader_cli():
    """Install and manage mod loaders (Forge, Fabric).
    
    A mod loader allows you to run mods and modpacks.
    Each loader creates a new Minecraft version that can be used in instances."""
    pass


for loader in mod.LOADERS:
    loader.register_cli(loader_cli)


def register_mod_cli(zeptomc_cli):
    zeptomc_cli.add_command(mod_cli, name="mod")
