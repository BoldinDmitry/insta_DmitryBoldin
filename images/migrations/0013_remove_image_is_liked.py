# Generated by Django 2.2.6 on 2019-11-04 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0012_auto_20191104_2205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='is_liked',
        ),
    ]