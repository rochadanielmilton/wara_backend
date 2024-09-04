import os
import sys
from django.conf import settings
from django.urls import get_resolver
from backend_mmaya.env import BASE_DIR, env
env.read_env(os.path.join(BASE_DIR,'.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', env("DJANGO_SETTINGS_MODULE"))
import django
django.setup()

def list_urls():
    urlconf = settings.ROOT_URLCONF
    resolver = get_resolver(urlconf)

    def _iterate_patterns(patterns, prefix=''):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                yield from _iterate_patterns(pattern.url_patterns, prefix + pattern.pattern.regex.pattern)
            else:
                yield prefix + pattern.pattern.regex.pattern

    for url in _iterate_patterns(resolver.url_patterns):
        print(url)

if __name__ == '__main__':
    list_urls()