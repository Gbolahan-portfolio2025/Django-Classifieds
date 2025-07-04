# Generated by Django 5.2.2 on 2025-06-14 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='expires_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ad',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]
