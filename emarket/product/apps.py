from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'
from django.apps import AppConfig
import os
from django.apps import AppConfig
import os

class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        if os.environ.get("LOAD_FIXTURE", "false") == "true":
            from django.core.management import call_command
            try:
                call_command("loaddata", "all_data.json")
                print("✅ Fixture loaded successfully!")
            except Exception as e:
                print("❌ Error loading fixture:", e)
