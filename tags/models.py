from django.db import models
from tasks.models import Task

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    tasks = models.ManyToManyField(Task, related_name='tags', blank=True)

    def __str__(self):
        return self.name
