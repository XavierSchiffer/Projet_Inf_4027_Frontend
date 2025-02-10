from django.apps import AppConfig


class FruitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Fruit'

    def ready(self):
        import Fruit.signals  # Importer les signaux


