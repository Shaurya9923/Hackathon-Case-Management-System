# Generated by Django 3.0.8 on 2020-07-28 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0008_auto_20200729_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='opponent_address',
            field=models.TextField(null=True),
        ),
    ]