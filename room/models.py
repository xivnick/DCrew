from django.db import models
from django.conf import settings
from game.models import Game


# Create your models here.
class Room(models.Model):

    CAPACITY_CHOICES = (
        ('', '인원 선택'),
        (3, '3 명'),
        (4, '4 명'),
        (5, '5 명'),
    )

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField(
        choices=CAPACITY_CHOICES,
    )
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.title


class RoomUser(models.Model):

    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    seat = models.IntegerField(null=True)
    connect = models.BooleanField(default=True)

    class Meta:
        unique_together = ('room', 'seat',)

    def __str__(self):
        return '(r:"' + str(self.room) + '", u:"' + str(self.user) + '")'
