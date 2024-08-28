
from django.db import models

class DataInformation(models.Model):
    name = models.CharField(max_length=255)
    storage_location = models.CharField(max_length=255)
    access_list = models.TextField()
    size = models.FloatField()  # Size in GB
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
