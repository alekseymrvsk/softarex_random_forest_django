from django.db import models

from users.models import UserProfile


class Files(models.Model):
    file = models.FileField(upload_to='input_user/%Y-%m-%d/')
    file_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)


