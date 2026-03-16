import json
import urllib.parse
from datetime import datetime, timezone

import click
import requests

from zeptomc.cli.utils import pass_launcher
from zeptomc.logging import logger
from zeptomc.utils import Directory, die

_loader_name = "fabric"

PACKAGE = "net.fabricmc"
MAVEN_BASE = "https://maven.fabricmc.net/"
LOADER_NAME = "fabric-loader"
MAPPINGS_NAME = "intermediary"

__all__ = ["register_cli"]


class VersionError(Exception):
    pass


def latest_game_version():
    url = "https://meta.fabricmc.net/v2/versions/game"
    obj = requests.get(url).json()
    for ver in obj:
        if ver["stable"]:
            return ver["version"]


def get_loader_meta(game_version, loader_version):
    url = "https://meta.fabricmc.net/v2/versions/loader/{}".format(
        urllib.parse.quote(game_version)
    )
    obj = requests.get(url).json()
    if len(obj) == 0:
        raise VersionError("Specified game version is unsupported")
    if loader_version is None:
        ver = next(v for v in obj if v["loader"]["stable"])
    else:
        try:
            ver = next(v for v in obj if v["loader"]["version"] == loader_version)
        except StopIteration:
            raise VersionError("Specified loader version is not available") from None
    return ver["loader"]["version"], ver["launcherMeta"]


def resolve_version(game_version=None, loader_version=None):
    if game_version is None:
        game_version = latest_game_version()

    loader_version, loader_obj = get_loader_meta(game_version, loader_version)
    return game_version, loader_version, loader_obj


def generate_vspec_obj(version_name, loader_obj, loader_version, game_version):
    out = dict()

    out["id"] = version_name
    out["inheritsFrom"] = game_version
    out["jar"] = game_version  # Prevent the jar from being duplicated

    current_time = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    out["time"] = current_time

    mainClass = loader_obj["mainClass"]
    if isinstance(mainClass, dict):
        mainClass = mainClass["client"]
    out["mainClass"] = mainClass

    libs = []
    for side in ["common", "client"]:
        libs.extend(loader_obj["libraries"][side])

    for artifact, version in [
        (MAPPINGS_NAME, game_version),
        (LOADER_NAME, loader_version),
    ]:
        libs.append(
            {"name": "{}:{}:{}".format(PACKAGE, artifact, version), "url": MAVEN_BASE}
        )

    out["libraries"] = libs

    return out


def install(versions_root, game_version=None, loader_version=None, version_name=None):
    game_version, loader_version, loader_obj = resolve_version(
        game_version, loader_version
    )

    if version_name is None:
        version_name = "{}-{}-{}".format(LOADER_NAME, loader_version, game_version)

    version_dir = versions_root / version_name
    if version_dir.exists():
        die(f"Version with name {version_name} already exists")

    msg = f"Installing Fabric version {loader_version}-{game_version}"
    if version_name:
        msg += f" as {version_name}"
    logger.info(msg)

    vspec_obj = generate_vspec_obj(
        version_name, loader_obj, loader_version, game_version
    )

    version_dir.mkdir()
    with open(version_dir / f"{version_name}.json", "w") as fd:
        json.dump(vspec_obj, fd, indent=2)


@click.command("fabric")
@click.argument("game_version", required=False)
@click.argument("loader_version", required=False)
@click.option("--name", default=None, help="Custom name for the installed version")
@pass_launcher
def fabric_cli(launcher, game_version, loader_version, name):
    """Install the Fabric mod loader.

    GAME_VERSION is optional. If omitted, the latest stable Minecraft version
    is used. LOADER_VERSION is also optional; the latest stable loader for the
    given game version is selected automatically.

    \b
    Examples:
      zeptomc install fabric
      zeptomc install fabric 1.20.1
      zeptomc install fabric 1.20.1 0.15.3"""
    versions_root = launcher.get_path(Directory.VERSIONS)
    try:
        install(
            versions_root,
            game_version,
            loader_version,
            version_name=name,
        )
    except VersionError as e:
        logger.error(e)


def register_cli(root):
    root.add_command(fabric_cli)
