from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class News(models.Model):
    source = models.CharField(max_length=255)
    headline = models.TextField()
    reportedAt = models.DateTimeField(null=True, blank=True)
    link = models.URLField()

    class Meta:
      verbose_name_plural = "news"

    def __str__(self):
        return self.source