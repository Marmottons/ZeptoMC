import click

from zeptomc.account import (
    AccountError,
    MicrosoftAccount,
    OfflineAccount,
    RefreshError,
)
from zeptomc.cli.utils import pass_account_manager
from zeptomc.logging import logger


def account_cmd(fn):
    return click.argument("account")(fn)


@click.group()
def account_cli():
    """Manage your accounts."""
    pass


@account_cli.command("list")
@pass_account_manager
def _list(am):
    """List avaiable accounts."""
    alist = am.list()
    if alist:
        lines = ("{}{}".format("* " if am.is_default(u) else "  ", u) for u in alist)
        print("\n".join(lines))
    else:
        logger.info("No accounts.")


@account_cli.command()
@account_cmd
@pass_account_manager
def create(am, account):
    """Create an offline account."""
    try:
        acc = OfflineAccount.new(am, account)
        am.add(acc)
        logger.info(f"Offline account '{account}' created successfully")
    except AccountError as e:
        logger.error("Could not create account: %s", e)


@account_cli.command()
@account_cmd
@pass_account_manager
def authenticate(am, account):
    """Authenticate a Microsoft account (creates it if it doesn't exist)."""

    try:
        a = am.get(account)
        # Account exists
        if isinstance(a, OfflineAccount):
            logger.error("Offline accounts do not require authentication")
            return
    except AccountError:
        # Account doesn't exist, create a new Microsoft account
        a = MicrosoftAccount.new(am, account)
        am.add(a)
        logger.info(f"Created new Microsoft account: {account}")

    # Authenticate Microsoft account
    try:
        if isinstance(a, MicrosoftAccount):
            a.authenticate()
            logger.info(f"Account '{account}' authenticated successfully")
        else:
            logger.error("Unknown account type")
    except Exception as e:
        logger.error("Authentication failed: %s", e)


@account_cli.command()
@account_cmd
@pass_account_manager
def refresh(am, account):
    """Refresh access token for a Microsoft account."""
    try:
        a = am.get(account)
        a.refresh()
    except (AccountError, RefreshError) as e:
        logger.error("Could not refresh account: %s", e)


@account_cli.command()
@account_cmd
@pass_account_manager
def remove(am, account):
    """Remove the account."""
    try:
        am.remove(account)
    except AccountError as e:
        logger.error("Could not remove account: %s", e)


@account_cli.command()
@account_cmd
@pass_account_manager
def setdefault(am, account):
    """Set the account as default."""
    try:
        default = am.get(account)
        am.set_default(default)
    except AccountError as e:
        logger.error("Could not set default account: %s", e)


def register_account_cli(zeptomc_cli):
    zeptomc_cli.add_command(account_cli, name="account")
