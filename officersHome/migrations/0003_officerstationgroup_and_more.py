# Generated by Django 5.0.6 on 2024-05-18 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officersHome', '0002_newofficerregistration_officer_stationrank'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficerStationGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.CharField(max_length=250)),
                ('user_count', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='newofficerregistration',
            name='officer_profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profileImages/'),
        ),
    ]
