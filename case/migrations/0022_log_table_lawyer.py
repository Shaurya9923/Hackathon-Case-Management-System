# Generated by Django 3.0.8 on 2020-08-02 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0021_log_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='log_table',
            name='lawyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='case.lawyers'),
        ),
    ]