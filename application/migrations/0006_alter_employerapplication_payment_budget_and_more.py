# Generated by Django 4.0.3 on 2022-05-14 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_alter_employerapplication_payment_budget_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerapplication',
            name='payment_budget',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='payment_budget',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
