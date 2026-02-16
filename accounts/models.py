from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid

class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)

    is_email_verified = models.BooleanField(default=False)

    email_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",
        blank=True
    )

    REQUIRED_FIELDS = []
