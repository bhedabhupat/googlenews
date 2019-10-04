from django.db import models


# Create your models here.

class RssData(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    guid = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    description = models.TextField()
    source = models.CharField(max_length=200)
