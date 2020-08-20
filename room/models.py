from django.db import models


# Create your models here.
class Room(models.Model):

    STATUS_CHOICES = (
        ('W', 'Waiting'),
        ('I', 'In Game'),
    )

    id = models.AutoField(primary_key=True)
    hostId = models.IntegerField()
    title = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='W'
    )
    gameId = models.IntegerField()

    def __str__(self):
        return self.title


class RoomPlayer(models.Model):

    id = models.AutoField(primary_key=True)
    roomId = models.IntegerField()
    playerId = models.IntegerField()

    def __str__(self):
        return '(' + str(self.roomId) + ', ' + str(self.playerId) + ')'
