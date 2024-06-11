from django.contrib.auth.models import User
from django.db import models


class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="test")
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.title