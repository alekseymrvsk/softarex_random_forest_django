from django.db import models


class Files(models.Model):
    file = models.FileField(upload_to='input_user/%Y-%m-%d/')