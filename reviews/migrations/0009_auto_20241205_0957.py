# Generated by Django 3.1.12 on 2024-12-05 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_review_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.JSONField(),
        ),
    ]
