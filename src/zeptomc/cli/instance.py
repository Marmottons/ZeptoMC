import functools

import click

from zeptomc.cli.utils import pass_instance_manager, pass_launcher
from zeptomc.logging import logger
from zeptomc.utils import Directory, die, sanitize_name


def instance_cmd(fn):
    @click.argument("instance_name")
    @functools.wraps(fn)
    def inner(*args, instance_name, **kwargs):
        return fn(*args, instance_name=sanitize_name(instance_name), **kwargs)

    return inner


@click.group()
def instance_cli():
    """Manage game instances.
    
    An instance is a directory with its own Minecraft version, mods, and settings.
    You can have multiple instances with different versions or configurations.
    
    Examples:
      zeptomc instance add vanilla          # Create vanilla 1.20.1
      zeptomc instance add forge18 1.18.2   # Create 1.18.2 with Forge
      zeptomc instance mv old-name new-name  # Rename an instance
      zeptomc instance ls                   # Show all instances"""
    pass


@instance_cli.command("add")
@instance_cmd
@click.argument("version", default="latest")
@pass_instance_manager
def add(im, instance_name, version):
    """Create a new instance.
    
    Usage: zeptomc instance add INSTANCE [VERSION]
    
    Examples:
      zeptomc instance add my-world           # Latest version
      zeptomc instance add retro-game 1.12.2  # Specific version"""
    if im.exists(instance_name):
        logger.error(f"An instance named '{instance_name}' already exists.\nUse 'zeptomc instance ls' to see all instances.")
        return
    im.create(instance_name, version)


@instance_cli.command("ls")
@pass_instance_manager
def ls(im):
    """Show all instances.
    
    Example: zeptomc instance ls"""
    print("\n".join(im.list()))


@instance_cli.command("rm")
@instance_cmd
@pass_instance_manager
def rm(im, instance_name):
    """Delete an instance permanently (cannot be undone)."""
    if im.exists(instance_name):
        im.delete(instance_name)
    else:
        logger.error(f"No instance named '{instance_name}' exists.\nUse 'zeptomc instance ls' to see all instances.")


@instance_cli.command("dir")
@click.argument("instance_name", required=False)
@pass_instance_manager
@pass_launcher
def _dir(launcher, im, instance_name):
    """Print root directory of instance."""
    if not instance_name:
        print(launcher.get_path(Directory.INSTANCES))
    else:
        instance_name = sanitize_name(instance_name)
        print(im.get_root(instance_name))


@instance_cli.command("mv")
@instance_cmd
@click.argument("new_name")
@pass_instance_manager
def mv(im, instance_name, new_name):
    """Rename/move an instance.
    
    Example: zeptomc instance mv old-name new-name"""
    new_name = sanitize_name(new_name)
    if im.exists(instance_name):
        if im.exists(new_name):
            die("Instance with target name already exists.\nUse 'zeptomc instance ls' to see all instances.")
        im.rename(instance_name, new_name)
    else:
        die(f"No instance named '{instance_name}' exists.\nUse 'zeptomc instance ls' to see all instances.")

def register_instance_cli(zeptomc_cli):
    zeptomc_cli.add_command(instance_cli, name="instance")
