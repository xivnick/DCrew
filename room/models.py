from django.db import models


# Create your models here.
class Room(models.Model):

    STATUS_CHOICES = (
        ('W', 'Waiting'),
        ('I', 'In Game'),
    )

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
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='W',
    )
    gameId = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class RoomUser(models.Model):

    TYPE_CHOICES = (
        ('H', 'Host'),
        ('P', 'Player'),
        ('O', 'Observer'),
    )

    id = models.AutoField(primary_key=True)
    roomId = models.IntegerField()
    userId = models.IntegerField()
    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
    )

    def __str__(self):
        return '(' + str(self.roomId) + ', ' + str(self.userId) + ')'
