# Generated by Django 5.0.2 on 2024-02-17 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_isviewcustomer'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isdeletecustomer',
            field=models.BooleanField(default=False),
        ),
    ]