# Generated by Django 2.2.6 on 2019-10-30 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0003_auto_20191030_1129"),
    ]

    operations = [
        migrations.RenameField(
            model_name="creator", old_name="username", new_name="USERNAME_FIELD",
        ),
    ]