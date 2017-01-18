import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BOT_NAME = 'intelivix'

SPIDER_MODULES = ['AhNegao.spiders', 'GitHub.spiders']

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'intelivix',
    'password': 'intelivix',
    'database': 'intelivix',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'ahnegao': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/ahnegao.log'),
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'github': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/github.log'),
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'ahnegao': {
            'handlers': ['ahnegao'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'github': {
            'handlers': ['github'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

logging.config.dictConfig(LOGGING)
