# Generated by Django 3.1 on 2020-09-07 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_gameplayer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='playerNum',
        ),
    ]
