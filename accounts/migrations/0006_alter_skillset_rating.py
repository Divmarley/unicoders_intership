# Generated by Django 4.0.3 on 2022-05-19 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_account_type_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillset',
            name='rating',
            field=models.IntegerField(choices=[(10, 10), (20, 20), (30, 30), (40, 40), (50, 50), (60, 60), (70, 70), (80, 80), (90, 90), (100, 100)]),
        ),
    ]