# Generated by Django 3.1 on 2020-08-22 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
