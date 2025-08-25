from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'
from django.apps import AppConfig
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import os
        from django.core.management import call_command
        if os.environ.get("LOAD_FIXTURE", "false") == "true":
            try:
                call_command("loaddata", "all_data.json")
                print("✅ Fixture data loaded successfully!")
            except Exception as e:
                print("⚠️ Error loading fixture:", e)
