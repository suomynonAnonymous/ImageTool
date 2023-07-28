from django.db import models

# Create your models here.
class ProcessedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    processed = models.ImageField(upload_to='processed_images/', blank=True, null=True)