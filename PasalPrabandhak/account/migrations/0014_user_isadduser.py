# Generated by Django 5.0.2 on 2024-02-11 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_branch_branch_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isadduser',
            field=models.BooleanField(default=False),
        ),
    ]