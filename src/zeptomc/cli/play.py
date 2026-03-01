import getpass

import click

from zeptomc.account import AccountError, OfflineAccount, OnlineAccount
from zeptomc.cli.utils import pass_account_manager, pass_instance_manager, pass_launcher


@click.command()
@click.argument("target", required=False)
@click.option("-a", "--account", "account_name")
@click.option("--verify", is_flag=True, default=False)
@pass_instance_manager
@pass_account_manager
@pass_launcher
def play(launcher, am, im, target, account_name, verify):
    """Play Minecraft with a version or instance.
    
    TARGET can be:
    - A version (e.g., '1.20.1') - launches default instance
    - An instance name - launches that instance with its version
    - Empty - launches default instance with latest version
    """
    if account_name:
        account = am.get(account_name)
    else:
        try:
            account = am.get_default()
        except AccountError:
            username = input("Choose your account name:\n> ")
            email = input(
                "\nIf you have a mojang account with a Minecraft license,\n"
                "enter your email. Leave blank if you want to play offline:\n> "
            )
            if email:
                account = OnlineAccount.new(am, username, email)
            else:
                account = OfflineAccount.new(am, username)
            am.add(account)
            if email:
                password = getpass.getpass("\nPassword:\n> ")
                account.authenticate(password)
    
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
    
    inst.launch(account, version, verify_hashes=verify)


def register_play_cli(zeptomc_cli):
    zeptomc_cli.add_command(play)
