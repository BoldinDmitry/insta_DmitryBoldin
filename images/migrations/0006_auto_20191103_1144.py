# Generated by Django 2.2.6 on 2019-11-03 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0005_auto_20191030_1149"),
    ]

    operations = [
        migrations.AlterField(
            model_name="creator",
            name="followers_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="creator",
            name="following_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="creator",
            name="post_count",
            field=models.IntegerField(default=0),
        ),
    ]