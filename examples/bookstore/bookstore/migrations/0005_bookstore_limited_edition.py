# Generated by Django 4.2.20 on 2025-04-28 22:36

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bookstore", "0004_bookstore_release_dt"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookstore",
            name="limited_edition",
            field=models.BooleanField(default=False, null=True),
        ),
    ]
