# Generated by Django 4.0.3 on 2022-05-10 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='date',
            new_name='start',
        ),
    ]
