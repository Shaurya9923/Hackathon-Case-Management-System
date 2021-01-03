# Generated by Django 3.0.8 on 2020-08-03 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0028_auto_20200803_1300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cases',
            old_name='action_on_final_order',
            new_name='action_taken',
        ),
        migrations.AddField(
            model_name='cases',
            name='decision',
            field=models.TextField(blank=True, null=True),
        ),
    ]
