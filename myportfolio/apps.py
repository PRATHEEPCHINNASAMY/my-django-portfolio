from django.apps import AppConfig
from django.db.models.signals import post_migrate

class MyportfolioConfig(AppConfig):
    name = 'myportfolio'
    def ready(self):
        from myportfolio.signals import create_group_permissions
        post_migrate.connect(create_group_permissions)