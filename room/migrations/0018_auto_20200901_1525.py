# Generated by Django 3.1 on 2020-09-01 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0017_auto_20200901_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomuser',
            name='seat',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='roomuser',
            unique_together={('room', 'seat')},
        ),
    ]