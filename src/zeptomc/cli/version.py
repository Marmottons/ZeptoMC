import functools
import os
import posixpath
import urllib.parse

import click

from zeptomc.cli.utils import pass_version_manager
from zeptomc.logging import logger
from zeptomc.utils import die, file_sha1
from zeptomc.version import VersionType


def version_cmd(fn):
    @click.argument("version_name")
    @pass_version_manager
    @functools.wraps(fn)
    def inner(vm, *args, version_name, **kwargs):
        return fn(*args, version=vm.get_version(version_name), **kwargs)

    return inner


@click.group()
def version_cli():
    """Manage Minecraft versions.
    
    Download and manage different Minecraft versions.
    By default shows only locally installed versions.
    
    Examples:
      zeptomc version list                # Show installed versions
      zeptomc version list --all          # Show all available versions
      zeptomc version prepare 1.20.1      # Download version 1.20.1"""
    pass


@version_cli.command()
@click.option("--release", is_flag=True, default=False, help="Show release versions")
@click.option("--snapshot", is_flag=True, default=False, help="Show snapshot versions")
@click.option("--alpha", is_flag=True, default=False, help="Show alpha versions")
@click.option("--beta", is_flag=True, default=False, help="Show beta versions")
@click.option("--local", is_flag=True, default=False, help="Show locally installed")
@click.option("--all", is_flag=True, default=False, help="Show all available versions")
@pass_version_manager
def list(vm, release, snapshot, alpha, beta, local, all):
    """List available Minecraft versions."""
    if all:
        release = snapshot = alpha = beta = local = True
    elif not (release or snapshot or alpha or beta):
        logger.info(
            "Showing only locally installed versions. "
            "Use `version list --help` to get more info."
        )
        local = True
    T = VersionType.create(release, snapshot, alpha, beta)
    versions = vm.version_list(vtype=T, local=local)
    print("\n".join(versions))


@version_cli.command()
@version_cmd
@click.option("--verify", is_flag=True, default=False, help="Verify file integrity")
def prepare(version, verify):
    """Download and prepare a Minecraft version.
    
    Usage: zeptomc version prepare VERSION [OPTIONS]
    
    Example:
      zeptomc version prepare 1.20.1"""
    version.prepare(verify_hashes=verify)


@version_cli.command()
@version_cmd
@click.argument("which", default="client")
@click.option("--output", default=None)
def jar(version, which, output):
    """Download the file and save."""
    dlspec = version.vspec.downloads.get(which, None)
    if not dlspec:
        die("No such dlspec exists for version {}".format(version.version_name))
    url = dlspec["url"]
    sha1 = dlspec["sha1"]
    ext = posixpath.basename(urllib.parse.urlsplit(url).path).split(".")[-1]
    if output is None:
        output = "{}_{}.{}".format(version.version_name, which, ext)
    if os.path.exists(output):
        die("Refusing to overwrite {}".format(output))
    logger.info("Hash (sha1) should be {}".format(sha1))
    logger.info("Downloading the {} file and saving to {}".format(which, output))
    urllib.request.urlretrieve(dlspec["url"], output)
    if file_sha1(output) != sha1:
        logger.warning("Hash of downloaded file does not match")


def register_version_cli(root_cli):
    root_cli.add_command(version_cli, "version")
