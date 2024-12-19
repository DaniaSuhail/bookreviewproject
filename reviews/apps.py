from django.apps import AppConfig
from django.apps import AppConfig

class ReviewsConfig(AppConfig):
    name = "reviews"

    def ready(self):
        import reviews.signals




