# Generated by Django 5.0.2 on 2024-02-14 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='attandance',
            name='ip_address',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]