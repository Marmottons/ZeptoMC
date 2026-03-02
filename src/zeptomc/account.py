import uuid

from zeptomc.errors import RefreshError, ValidationError
from zeptomc.logging import logger
from zeptomc.msapi import MicrosoftAuthApi


class NAMESPACE_NULL:
    bytes = b""


def generate_client_token():
    # Any random string, this matches the behaviour of the official launcher.
    return str(uuid.uuid4().hex)


class Account:
    def __init__(self, **kwargs):
        self.__dict__.update(self.DEFAULTS)
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.name

    def to_dict(self):
        return {k: getattr(self, k) for k in self.DEFAULTS.keys()}

    def save(self):
        self._am.save(self)

    @classmethod
    def from_config(cls, am, name, config):
        if config.get("microsoft", False):
            c = MicrosoftAccount
        else:
            c = OfflineAccount
        return c(name=name, _am=am, **config)


class OfflineAccount(Account):
    DEFAULTS = {"uuid": "-", "online": False}
    access_token = "-"

    @classmethod
    def new(cls, am, name):
        u = uuid.uuid3(NAMESPACE_NULL, "OfflinePlayer:{}".format(name)).hex
        return cls(name=name, uuid=u, _am=am)

    @property
    def gname(self):
        return self.name

    def refresh(self):
        return False

    def can_launch_game(self):
        return True


class MicrosoftAccount(Account):
    DEFAULTS = {
        "uuid": "-",
        "online": True,
        "microsoft": True,
        "gname": "-",
        "access_token": "-",
        "refresh_token": "-",
        "is_authenticated": False,
    }

    @classmethod
    def new(cls, am, name):
        return cls(name=name, _am=am)

    def refresh(self, force=False):
        if not self.is_authenticated:
            raise RefreshError("Account is not authenticated, cannot refresh")
        try:
            valid = self._am.msapi.validate(self.access_token)
        except ValidationError as e:
            raise RefreshError(e)
        if valid:
            logger.debug("msa: token still valid")
            return False
        else:
            logger.debug("msa: token not valid anymore, refreshing")
            self.access_token, self.refresh_token = self._am.msapi.refresh(
                self.refresh_token
            )
            self.save()
            return True

    def authenticate(self):
        self.access_token, self.refresh_token = self._am.msapi.authenticate()
        profile = self._am.msapi.get_profile(self.access_token)
        self.gname = profile["name"]
        self.uuid = profile["id"]
        self.is_authenticated = True
        self.save()

    def can_launch_game(self):
        return self.is_authenticated


class AccountError(ValueError):
    def __str__(self):
        return " ".join(self.args)


DEFAULT_CONFIG = {
    "default": None,
    "accounts": {},
    "client_token": generate_client_token(),
}


class AccountManager:
    CONFIG_FILE = "accounts.json"

    def __init__(self, launcher):
        self.config = launcher.config_manager.get(self.CONFIG_FILE, init=DEFAULT_CONFIG)
        self.msapi = MicrosoftAuthApi()

    def list(self):
        return self.config["accounts"].keys()

    def get(self, name):
        try:
            acc = Account.from_config(self, name, self.config["accounts"][name])
            acc.is_default = self.config["default"] == name
            return acc
        except KeyError as ke:
            raise AccountError("Account does not exist:", name) from ke

    def exists(self, name):
        return name in self.config["accounts"]

    def get_default(self):
        default = self.config["default"]
        if not default:
            raise AccountError("Default account not configured.")
        return self.get(default)

    def is_default(self, name):
        return name == self.config["default"]

    def set_default(self, account):
        self.config["default"] = account.name

    def add(self, account):
        if self.exists(account.name):
            raise AccountError("An account already exists with that name.")
        if not self.config["default"] and not self.config["accounts"]:
            self.config["default"] = account.name
        self.save(account)

    def save(self, account):
        self.config["accounts"][account.name] = account.to_dict()
        self.config.dirty = True

    def remove(self, name):
        try:
            if self.config["default"] == name:
                self.config["default"] = None
            del self.config["accounts"][name]
            self.config.dirty = True
        except KeyError:
            raise AccountError("Account does not exist:", name)
