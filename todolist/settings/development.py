from .base import *

INSTALLED_APPS += [
    "drf_yasg",
]

DEBUG = True

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

ALLOWED_HOSTS = ["testserver", "localhost"]
