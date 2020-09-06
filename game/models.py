from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


# Create your models here.
class Game(models.Model):

    STATUS_CHOICES = (
        ('P', 'Playing'),
        ('E', 'End'),
    )

    MODE_CHOICES = (
        ('', '모드 선택'),
        ('O', 'Original'),
        ('C', 'Casual'),
    )

    id = models.AutoField(primary_key=True)
    playerNum = models.IntegerField(
        choices=((3, 3), (4, 4), (5, 5)),
    )
    mode = models.CharField(
        max_length=1,
        choices=MODE_CHOICES,
    )
    stage = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(50), MinValueValidator(1)]
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='P',
    )


class GamePlayer(models.Model):

    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
    )
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    pid = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self):
        return '(g:"' + str(self.game) + '", p:"' + str(self.player) + '")'
