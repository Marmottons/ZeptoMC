import click

from zeptomc import mod
from zeptomc.cli.utils import pass_launcher
from zeptomc.logging import logger
from zeptomc.mod.forge import AlreadyInstalledError, InstallationError, VersionResolutionError
from zeptomc.mod.fabric import VersionError
from zeptomc.utils import Directory
from zeptomc.version import VersionType


@click.command()
@click.argument("target", required=False)
@click.argument("loader", required=False)
@click.option("--release", is_flag=True, default=False, help="Show release versions")
@click.option("--snapshot", is_flag=True, default=False, help="Show snapshot versions")
@click.option("--all", is_flag=True, default=False, help="Show all available versions")
@click.option("--name", default=None, help="Custom name for the installed version")
@pass_launcher
def install_cli(launcher, target, loader, release, snapshot, all, name):
    """Install Minecraft versions and mod loaders.

    \b
    TARGET can be a version number, a mod loader (forge/fabric), or 'ls'.

    \b
    Examples:
      zeptomc install              Install latest vanilla version
      zeptomc install ls           List available versions
      zeptomc install 1.20.1       Install vanilla 1.20.1
      zeptomc install forge        Latest version with Forge
      zeptomc install 1.20.1 forge Install 1.20.1 with Forge
      zeptomc install 1.20.1 fabric Install 1.20.1 with Fabric"""
    vm = launcher.version_manager

    if target == "ls":
        if all:
            release = snapshot = True
        elif not (release or snapshot):
            logger.info(
                "Showing only locally installed versions. "
                "Use --all to see all."
            )
        T = VersionType.create(release, snapshot, False, False)
        versions = vm.version_list(vtype=T, local=not all and not release and not snapshot)
        print("\n".join(versions))
        return

    game_version = target
    loader_mod = None

    if target is None:
        game_version = vm.resolve_version_name("latest")
    elif target.lower() in ("forge", "fabric"):
        loader_mod = getattr(mod, target.lower())
        game_version = vm.resolve_version_name("latest")
    else:
        if loader and loader.lower() in ("forge", "fabric"):
            loader_mod = getattr(mod, loader.lower())

    logger.info(f"Preparing Minecraft {game_version}")
    version_obj = vm.get_version(game_version)
    version_obj.prepare()

    if loader_mod:
        versions_root = launcher.get_path(Directory.VERSIONS)
        logger.info(f"Installing {loader_mod._loader_name} for {game_version}")
        try:
            if loader_mod is mod.forge:
                libraries_root = launcher.get_path(Directory.LIBRARIES)
                mod.forge.install(versions_root, libraries_root, game_version=game_version, version_name=name)
            else:
                mod.fabric.install(versions_root, game_version=game_version, version_name=name)
        except (VersionResolutionError, InstallationError, AlreadyInstalledError, VersionError) as e:
            logger.error(e)


def register_install_cli(zeptomc_cli):
    zeptomc_cli.add_command(install_cli, name="install")
