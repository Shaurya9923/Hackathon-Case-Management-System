# Generated by Django 3.0.8 on 2020-07-24 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200724_2232'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='organiation',
            new_name='organization',
        ),
    ]
