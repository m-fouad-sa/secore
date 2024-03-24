from .base import *
from .base import env



DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY",
                 default="django-insecure-_+^!j=6^^6%m)q-br9*y640fth51zt&w+ii5l0n5z=7#9jrn)8")

ALLOWED_HOSTS = ["localhost","0.0.0.0","127.0.0.1"]