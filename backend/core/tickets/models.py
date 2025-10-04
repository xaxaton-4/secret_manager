from django.contrib.auth.models import User
from django.db import models


class Ticket(models.Model):
    resource = models.CharField(max_length=120)
    reason = models.CharField(max_length=120)
    period = models.DateField()
    is_approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
