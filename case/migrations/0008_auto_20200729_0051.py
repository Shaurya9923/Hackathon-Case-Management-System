# Generated by Django 3.0.8 on 2020-07-28 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0007_auto_20200728_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='description',
            field=models.TextField(null=True),
        ),
    ]