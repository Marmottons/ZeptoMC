import functools

import click

from zeptomc.account import AccountError
from zeptomc.cli.utils import pass_account_manager, pass_instance_manager, pass_launcher
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
      zeptomc instance create vanilla          # Create vanilla 1.20.1
      zeptomc instance create forge18 1.18.2   # Create 1.18.2 with Forge
      zeptomc instance list                    # Show all instances"""
    pass


@instance_cli.command()
@instance_cmd
@click.argument("version", default="latest")
@pass_instance_manager
def create(im, instance_name, version):
    """Create a new instance.
    
    Usage: zeptomc instance create INSTANCE [VERSION]
    
    Examples:
      zeptomc instance create my-world           # Latest version
      zeptomc instance create retro-game 1.12.2  # Specific version"""
    if im.exists(instance_name):
        logger.error(f"An instance named '{instance_name}' already exists.\nUse 'zeptomc instance list' to see all instances.")
        return
    im.create(instance_name, version)


@instance_cli.command()
@pass_instance_manager
def list(im):
    """Show all instances.
    
    Example: zeptomc instance list"""
    print("\n".join(im.list()))


@instance_cli.command()
@instance_cmd
@pass_instance_manager
def delete(im, instance_name):
    """Delete an instance permanently (cannot be undone)."""
    if im.exists(instance_name):
        im.delete(instance_name)
    else:
        logger.error(f"No instance named '{instance_name}' exists.\nUse 'zeptomc instance list' to see all instances.")


@instance_cli.command()
@instance_cmd
@click.option("--verify", is_flag=True, default=False, help="Verify file integrity")
@click.option("-a", "--account", default=None, help="Account to use (default: saved account)")
@click.option("--version-override", default=None, help="Override instance version")
@pass_instance_manager
@pass_account_manager
def launch(am, im, instance_name, account, version_override, verify):
    """Launch a specific instance.
    
    Usage: zeptomc instance launch INSTANCE_NAME [OPTIONS]
    
    Examples:
      zeptomc instance launch my-world
      zeptomc instance launch my-world --account steve"""
    if account is None:
        account = am.get_default()
    else:
        account = am.get(account)
    if not im.exists(instance_name):
        logger.error(f"No instance named '{instance_name}' exists.\nUse 'zeptomc instance list' to see all instances.")
        return
    inst = im.get(instance_name)
    try:
        inst.launch(account, version_override, verify_hashes=verify)
    except AccountError as e:
        logger.error("Not launching due to account error: {}".format(e))


@instance_cli.command("natives")
@instance_cmd
@pass_instance_manager
def extract_natives(im, instance_name):
    """Extract natives and leave them on disk.
    
    Example: zeptomc instance natives my-world"""
    if not im.exists(instance_name):
        die(f"No instance named '{instance_name}' exists.\nUse 'zeptomc instance list' to see all instances.")
    inst = im.get(instance_name)
    inst.extract_natives()


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


@instance_cli.command("rename")
@instance_cmd
@click.argument("new_name")
@pass_instance_manager
def rename(im, instance_name, new_name):
    """Rename an instance.
    
    Example: zeptomc instance rename old-name new-name"""
    new_name = sanitize_name(new_name)
    if im.exists(instance_name):
        if im.exists(new_name):
            die("Instance with target name already exists.\nUse 'zeptomc instance list' to see all instances.")
        im.rename(instance_name, new_name)
    else:
        die(f"No instance named '{instance_name}' exists.\nUse 'zeptomc instance list' to see all instances.")


@instance_cli.group("config")
@instance_cmd
@pass_instance_manager
@click.pass_context
def config_cli(ctx, im, instance_name):
    """Configure instance settings.
    
    Manage Java path, JVM args, and other instance settings.
    
    Examples:
      zeptomc instance config my-world show
      zeptomc instance config my-world java-path /usr/bin/java
      zeptomc instance config my-world java-args -Xmx4G"""
    if im.exists(instance_name):
        ctx.obj = im.get(instance_name).config
    else:
        die(f"No instance named '{instance_name}' exists.\nUse 'zeptomc instance list' to see all instances.")


@config_cli.command("show")
@click.pass_obj
def config_show(config):
    """Display all instance configuration."""

    for k, v in config.items():
        print("{}: {}".format(k, v))


@config_cli.command("set")
@click.argument("key")
@click.argument("value")
@click.pass_obj
def config_set(config, key, value):
    """Set a configuration value.
    
    Usage: zeptomc instance config INSTANCE set KEY VALUE"""
    config[key] = value


@config_cli.command("get")
@click.argument("key")
@click.pass_obj
def config_get(config, key):
    """Get a configuration value."""
    try:
        print(config[key])
    except KeyError:
        print("No such item.")


@config_cli.command("delete")
@click.argument("key")
@click.pass_obj
def config_delete(config, key):
    """Delete a configuration key."""
    try:
        del config[key]
    except KeyError:
        print("No such item.")


@config_cli.command("java-path")
@click.argument("path")
@click.pass_obj
def config_java_path(config, path):
    """Set the Java executable path for this instance.
    
    Specify a custom Java installation for this instance.
    
    Usage: zeptomc instance config INSTANCE java-path PATH
    
    Examples:
      zeptomc instance config my-world java-path /usr/bin/java
      zeptomc instance config modded /usr/lib/jvm/java-21/bin/java"""
    config["java.path"] = path
    print(f"Java path set to: {path}")


@config_cli.command("java-args", context_settings=dict(ignore_unknown_options=True, allow_interspersed_args=False))
@click.argument("args", required=True, nargs=-1)
@click.pass_obj
def config_java_args(config, args):
    """Set the JVM arguments for this instance.
    
    Configure memory and performance settings for Java.
    
    Usage: zeptomc instance config INSTANCE java-args [ARGS]
    
    Examples:
      zeptomc instance config my-world java-args -Xmx4G -Xms1G
      zeptomc instance config modded java-args -XX:+UseG1GC -Xmx8G"""
    java_args = " ".join(args)
    config["java.jvmargs"] = java_args
    print(f"Java arguments set to: {java_args}")


def register_instance_cli(zeptomc_cli):
    zeptomc_cli.add_command(instance_cli, name="instance")
