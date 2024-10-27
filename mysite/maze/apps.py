from django.apps import AppConfig


class MazeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maze'

from django.apps import AppConfig


class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services'