from django.db import models


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
    hostId = models.IntegerField()
    gameId = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class RoomUser(models.Model):

    id = models.AutoField(primary_key=True)
    roomId = models.IntegerField()
    userId = models.IntegerField()
    seat = models.IntegerField(default=0)
    connect = models.BooleanField(default=True)

    def __str__(self):
        return '(' + str(self.roomId) + ', ' + str(self.userId) + ')'
