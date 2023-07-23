# Generated by Django 4.2.3 on 2023-07-10 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PSM', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=255, unique=True)),
                ('pprice', models.IntegerField()),
                ('ptag', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
