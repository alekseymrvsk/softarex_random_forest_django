from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    n_predict = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user

    def __str__(self):
        return str(self.user)
