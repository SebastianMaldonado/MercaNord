# Generated by Django 4.2.6 on 2023-11-24 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario', models.CharField(max_length=255)),
                ('contacto', models.IntegerField(blank=True, null=True)),
                ('instagram', models.CharField(max_length=255)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='item_images')),
            ],
        ),
    ]
