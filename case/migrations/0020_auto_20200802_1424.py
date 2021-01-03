# Generated by Django 3.0.8 on 2020-08-02 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0019_auto_20200802_1422'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cases',
            old_name='case_synposis',
            new_name='case_synopsis',
        ),
        migrations.RemoveField(
            model_name='cases',
            name='synopsis',
        ),
        migrations.AddField(
            model_name='cases',
            name='action_on_final_order',
            field=models.TextField(blank=True, null=True),
        ),
    ]