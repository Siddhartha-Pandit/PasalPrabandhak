# Generated by Django 5.0.2 on 2024-02-17 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='companyid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.company'),
        ),
    ]
