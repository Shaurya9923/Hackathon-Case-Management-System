# Generated by Django 3.0.8 on 2020-07-25 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200724_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contact_no',
            field=models.CharField(max_length=10, null=True),
        ),
    ]