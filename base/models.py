from django.db import models
from django.utils import timezone


# Create your models here.
class Notice(models.Model):

    id = models.AutoField(primary_key=True)
    text = models.TextField()
    regDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if len(self.text) > 10:
            return self.text[:10] + '...'

        return self.text
