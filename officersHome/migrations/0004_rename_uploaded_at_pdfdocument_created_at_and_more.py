# Generated by Django 5.0.6 on 2024-05-23 01:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officersHome', '0003_pdfdocument'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='pdfdocument',
            old_name='uploaded_at',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='pdfdocument',
            name='file',
        ),
        migrations.RemoveField(
            model_name='pdfdocument',
            name='title',
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='file_path',
            field=models.CharField(default=250, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='user',
            field=models.ForeignKey(default=50, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]