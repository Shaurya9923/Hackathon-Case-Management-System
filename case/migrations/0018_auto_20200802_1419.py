# Generated by Django 3.0.8 on 2020-08-02 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0017_auto_20200802_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='action_at_final_order',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='final_order',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='interim_order',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='rejoinder',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='reply',
            field=models.TextField(blank=True, null=True),
        ),
    ]
