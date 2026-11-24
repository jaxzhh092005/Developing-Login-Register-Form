from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_roles(sender, **kwargs):
    """Create the role groups and attach permissions to them (runs after `migrate`)."""
    from django.contrib.auth.models import Group, Permission

    member, _ = Group.objects.get_or_create(name="Member")      # no special permissions
    manager, _ = Group.objects.get_or_create(name="Manager")    # can see all profiles

    perm = Permission.objects.filter(codename="view_all_profiles").first()
    if perm:
        manager.permissions.add(perm)


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        post_migrate.connect(create_roles, sender=self)
