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
    """Manage Minecraft accounts.
    
    Supported types:
      • Offline: Play locally without authentication (default)
      • Microsoft: Use your Microsoft account (online play)
    
    Examples:
      zeptomc account create my-account
      zeptomc account authenticate ms-account
      zeptomc account list"""
    pass


@account_cli.command("list")
@pass_account_manager
def _list(am):
    """List all accounts (marked with *)."""
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
    """Create a new offline account.
    
    Usage: zeptomc account create ACCOUNT_NAME
    
    Examples:
      zeptomc account create Steve
      zeptomc account create my-offline-profile"""
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
    """Create and authenticate a Microsoft account.
    
    Usage: zeptomc account authenticate ACCOUNT_NAME
    
    This will:
      1. Create a new Microsoft account if it doesn't exist
      2. Launch Microsoft login in your browser
      3. Save your credentials locally
    
    Example:
      zeptomc account authenticate my-ms-account"""

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
    """Refresh a Microsoft account token.
    
    Usage: zeptomc account refresh ACCOUNT_NAME
    
    Example:
      zeptomc account refresh my-ms-account"""
    try:
        a = am.get(account)
        a.refresh()
    except (AccountError, RefreshError) as e:
        logger.error("Could not refresh account: %s", e)


@account_cli.command()
@account_cmd
@pass_account_manager
def remove(am, account):
    """Delete an account (cannot be undone).
    
    Usage: zeptomc account remove ACCOUNT_NAME
    
    Example:
      zeptomc account remove old-account"""
    try:
        am.remove(account)
    except AccountError as e:
        logger.error("Could not remove account: %s", e)


@account_cli.command()
@account_cmd
@pass_account_manager
def setdefault(am, account):
    """Set the default account for launching games.
    
    Usage: zeptomc account setdefault ACCOUNT_NAME
    
    Example:
      zeptomc account setdefault my-main-account"""
    try:
        default = am.get(account)
        am.set_default(default)
    except AccountError as e:
        logger.error("Could not set default account: %s", e)


def register_account_cli(zeptomc_cli):
    zeptomc_cli.add_command(account_cli, name="account")
