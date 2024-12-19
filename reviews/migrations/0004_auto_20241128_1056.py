# Generated by Django 3.1.12 on 2024-11-28 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_bookreview'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='summary',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='book',
            name='average_rating',
        ),
        migrations.RemoveField(
            model_name='book',
            name='publication_date',
        ),
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='book_images/'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(max_length=50),
        ),
    ]