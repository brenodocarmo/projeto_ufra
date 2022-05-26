import environ

from controleprojeto.settings.base import *

env = environ.Env()

#DEBUG = env.bool("DEBUG", False)
DEBUG = env.bool(True)
SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DATABASES = {
    "default": env.db(),
}