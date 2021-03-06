# Generated by Django 3.0.8 on 2020-07-25 03:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('case', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='case_hearings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hearing_at', models.DateField()),
                ('description', models.TextField()),
                ('detail_doc', models.FileField(null=True, upload_to='documents/hearings')),
                ('status', models.CharField(choices=[('SCHEDULED', 'SCHEDULED'), ('SKIPPED', 'SKIPPED'), ('DONE', 'DONE')], max_length=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='cases',
            name='detail_doc',
            field=models.FileField(null=True, upload_to='documents/cases'),
        ),
        migrations.CreateModel(
            name='case_lawyers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')], max_length=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case.cases')),
                ('lawyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case.lawyers')),
            ],
        ),
        migrations.CreateModel(
            name='case_invoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxable_total', models.FloatField()),
                ('gst', models.FloatField()),
                ('payment_status', models.CharField(choices=[('UNPAID', 'UNPAID'), ('PAID', 'PAID')], max_length=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case.cases')),
                ('hearing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case.case_hearings')),
                ('lawyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case.lawyers')),
            ],
        ),
        migrations.AddField(
            model_name='case_hearings',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case.cases'),
        ),
        migrations.AddField(
            model_name='case_hearings',
            name='prev_hearing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='case.case_hearings'),
        ),
        migrations.AddField(
            model_name='case_hearings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
