from django.contrib import admin

# Register your models here.
from .models import ProcessedImage

admin.site.register(ProcessedImage)
