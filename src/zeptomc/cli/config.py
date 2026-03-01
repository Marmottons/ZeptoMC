import click

from zeptomc.cli.utils import pass_global_config


@click.group()
def config_cli():
    """Configure global zeptomc settings.
    
    Manage application-wide preferences and options.
    Use 'instance config' for per-instance settings.
    
    Examples:
      zeptomc config show
      zeptomc config set key value
      zeptomc config get key"""
    pass


@config_cli.command()
@pass_global_config
def show(cfg):
    """Display all configuration settings."""

    for k, v in cfg.bottom.items():
        if k not in cfg:
            print("[default] {}: {}".format(k, v))
    for k, v in cfg.items():
        print("{}: {}".format(k, v))


@config_cli.command("set")
@click.argument("key")
@click.argument("value")
@pass_global_config
def _set(cfg, key, value):
    """Set a global configuration value.
    
    Usage: zeptomc config set KEY VALUE
    
    Examples:
      zeptomc config set java_path /usr/bin/java
      zeptomc config set minecraft_dir ~/.minecraft"""
    cfg[key] = value


@config_cli.command()
@click.argument("key")
@pass_global_config
def get(cfg, key):
    """Get and print a global configuration value.
    
    Usage: zeptomc config get KEY
    
    Examples:
      zeptomc config get java_path
      zeptomc config get minecraft_dir"""
    try:
        print(cfg[key])
    except KeyError:
        print("No such item.")


@config_cli.command()
@click.argument("key")
@pass_global_config
def delete(cfg, key):
    """Delete a key from the global configuration.
    
    Usage: zeptomc config delete KEY
    
    Examples:
      zeptomc config delete java_path
      zeptomc config delete minecraft_dir
    
    Note: Settings revert to defaults after deletion."""
    try:
        del cfg[key]
    except KeyError:
        print("No such item.")


def register_config_cli(zeptomc_cli):
    zeptomc_cli.add_command(config_cli, name="config")
