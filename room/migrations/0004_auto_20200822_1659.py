# Generated by Django 3.1 on 2020-08-22 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0003_auto_20200822_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(choices=[(3, '3'), (4, '4'), (5, '5')], default=5),
        ),
    ]
