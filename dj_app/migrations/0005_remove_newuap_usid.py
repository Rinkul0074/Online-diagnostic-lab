# Generated by Django 3.2.7 on 2021-10-08 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0004_newuap_usid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuap',
            name='usid',
        ),
    ]
