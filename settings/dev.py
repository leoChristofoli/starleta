
import os

INSTALLED_APPS = (
    'models',
)

SECRET_KEY = 'REPLACE_ME'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": f"{BASE_DIR}/db.sqlite3"}}