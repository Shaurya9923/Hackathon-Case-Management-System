# Generated by Django 3.0.8 on 2020-07-28 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('court', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='court',
            name='contact_no',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
