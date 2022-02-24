from django.db import models

# Create your models here.

class EntryModel(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=1000)
    def __str__(self):
        return self.title


class SearchModel(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title
