import uuid
from django.db import models


class LicenseKey(models.Model):
    key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    employee_name = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.key)
