# Generated by Django 3.1 on 2020-08-29 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0011_auto_20200828_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomuser',
            name='connect',
            field=models.BooleanField(default=True),
        ),
    ]
