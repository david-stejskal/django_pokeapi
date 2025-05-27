import logging
import os

import environ

from django_pokeapi import enums

__version__ = "1.0.0"

_log = logging.getLogger(__name__)


env = environ.Env()
ENVVAR_NAME = "POKEAPI_CONFIG"
if config_path := os.getenv(ENVVAR_NAME, "config/dev.env"):
    env.read_env(config_path)
    print(f"Settings loaded from '{config_path}'")

try:
    _e: enums.Environment = enums.Environment(env.str("ENVIRONMENT"))
except ValueError:
    _log.error(
        "ENVIRONMENT with value '%s' is invalid. Defaulting to 'dev'.",
        env.str("ENVIRONMENT"),
    )
    _e = enums.Environment.DEV

ENVIRONMENT = _e
