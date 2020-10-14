from django.db import models
from .storage import OverwriteStorage
import os

# Create your models here.
class ImageModel(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/',storage=OverwriteStorage())

    def __str__(self):
        return self.name
    