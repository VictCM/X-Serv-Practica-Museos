from django.db import models

# Create your models here.

class Museo(models.Model):
    Name = models.CharField(max_length=100, default="Null")
    Dir = models.CharField(max_length=100, default="Null")
    Info = models.TextField(default="Null")

    def __str__(self):
        return self.Name
