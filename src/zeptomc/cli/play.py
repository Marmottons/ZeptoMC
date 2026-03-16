import click

from zeptomc.account import AccountError, OfflineAccount, MicrosoftAccount
from zeptomc.cli.utils import pass_account_manager, pass_instance_manager, pass_launcher


@click.command()
@click.argument("target", required=False)
@click.option("-a", "--account", "account_name", help="Account to use (default: saved account)")
@click.option("--verify", is_flag=True, default=False, help="Verify file integrity")
@click.option("--version-override", default=None, help="Override the instance version")
@pass_instance_manager
@pass_account_manager
@pass_launcher
def play(launcher, am, im, target, account_name, verify, version_override):
    """Launch Minecraft instantly.
    
    TARGET can be:
      • Empty = Default instance, latest version
      • Version (e.g., '1.20.1') = Default instance, specific version
      • Instance name (e.g., 'vanilla') = That instance, its version
    
    Examples:
      zeptomc play
      zeptomc play 1.20.1
      zeptomc play my-modded-world
      zeptomc play my-modded-world --version-override 1.20.1
      zeptomc play --account steve"""
    if account_name:
        account = am.get(account_name)
    else:
        try:
            account = am.get_default()
        except AccountError:
            username = input("Choose your account name:\n> ")
            use_microsoft = input(
                "\nDo you have a Microsoft account? (y/n, default: n):\n> "
            ).lower() == "y"
            
            if use_microsoft:
                account = MicrosoftAccount.new(am, username)
                am.add(account)
                account.authenticate()
            else:
                account = OfflineAccount.new(am, username)
                am.add(account)
    
    # Determine if target is an instance name or a version
    instance_name = None
    version = None
    
    if target:
        if im.exists(target):
            # It's an instance name
            instance_name = target
        else:
            # It's a version (or will be used as version override)
            version = target
    
    # Use the specified instance or default
    if instance_name:
        inst = im.get(instance_name)
    else:
        if not im.exists("default"):
            im.create("default", "latest")
        inst = im.get("default")
    
    inst.launch(account, version_override or version, verify_hashes=verify)


def register_play_cli(zeptomc_cli):
    zeptomc_cli.add_command(play)
