# Generated by Django 4.1.1 on 2022-09-28 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contents", "0002_content_teste"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="content",
            name="teste",
        ),
    ]
