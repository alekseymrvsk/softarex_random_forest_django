from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    n_predict = models.ImageField()

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
