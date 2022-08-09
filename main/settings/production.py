from .base import *
import environ

env = environ.Env()

environ.Env.read_env()

DEBUG = False

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = tuple(env.list('ALLOWED_HOSTS', default=[]))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# try:
#     from .local import *
# except ImportError:
#     pass
