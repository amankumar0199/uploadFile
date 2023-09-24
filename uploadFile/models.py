from django.db import models

# Create your models here.
class uploadedFile(models.Model):
    fileId = models.AutoField(primary_key=True)
    fileName = models.CharField(max_length = 100)
    fileExt = models.CharField(max_length=20)
    short_url = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    