# Generated by Django 3.1 on 2020-08-28 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0010_auto_20200827_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='status',
        ),
        migrations.AlterField(
            model_name='roomuser',
            name='seat',
            field=models.IntegerField(default=0),
        ),
    ]