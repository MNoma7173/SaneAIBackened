# Generated by Django 4.2.3 on 2023-08-07 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PSM', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='phonenum',
        ),
    ]
