from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    n_predict = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user

    def __str__(self):
        return str(self.user)


class ResultFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.FileField(upload_to='prediction/user_output_data/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user

    def __str__(self):
        return str(self.user)

