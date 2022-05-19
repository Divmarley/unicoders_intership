# Generated by Django 4.0.3 on 2022-05-12 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_account_type'),
        ('application', '0002_alter_employerapplication_job_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerapplication',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_em_application', to='accounts.userprofile'),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_job_application', to='accounts.userprofile'),
        ),
    ]