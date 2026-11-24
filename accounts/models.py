from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20)

    class Meta:
        # AUTHORIZATION: a custom permission we can grant to roles (groups)
        permissions = [("view_all_profiles", "Can view all member profiles")]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.phone})"
