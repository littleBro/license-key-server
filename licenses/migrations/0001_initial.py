# Generated by Django 4.2.2 on 2023-06-21 22:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LicenseKey",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "key",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "employee_name",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
            ],
        ),
    ]