# Generated by Django 4.1.5 on 2024-02-12 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_user_isadduser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_billing_clerk',
            field=models.BooleanField(default=False),
        ),
    ]
