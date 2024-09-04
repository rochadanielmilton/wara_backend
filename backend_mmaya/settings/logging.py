import os
import logging
from logging.handlers import TimedRotatingFileHandler

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

log_dir = os.path.join(BASE_DIR, 'debug')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(log_dir, 'debug.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 14,
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file','console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file','console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
