# Generated by Django 4.2.6 on 2023-11-24 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='imagen',
        ),
    ]
