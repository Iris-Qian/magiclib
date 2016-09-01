from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    rating = models.CharField(max_length=10)
    rating_people = models.CharField(max_length=10)
    introduction = models.CharField(max_length=5000)

    def __unicode__(self):
        return self.title
