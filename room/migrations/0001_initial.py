# Generated by Django 3.1 on 2020-08-20 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('host', models.IntegerField()),
                ('title', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('W', 'Waiting'), ('I', 'In Game')], default='W', max_length=1)),
                ('gameId', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RoomPlayer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('roomId', models.IntegerField()),
                ('playerId', models.IntegerField()),
            ],
        ),
    ]
