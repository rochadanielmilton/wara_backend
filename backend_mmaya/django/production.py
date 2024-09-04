from .base import *
from backend_mmaya.env import env

DEBUG = False
ALLOW_HOSTS = env.list("ALLOWED_HOSTS",default=[])