from django.db import models

# Create your models here.
class Keywords(models.Model):
    keyword	= models.CharField(max_length=400)
    tag	= models.CharField(max_length=200)
    search_volume	= models.IntegerField(default=0)
    category	= models.CharField(max_length=200)
    exam_tag = models.CharField(max_length=200)
        # renames the instances of the model
        # with their title name
    def __str__(self):
        return self.keyword

class GoogleSerp(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.ForeignKey(Keywords, on_delete=models.CASCADE)
    rank = models.IntegerField()
    date = models.CharField(max_length=100)
    domain = models.CharField(max_length=600)
    url = models.TextField()
    def __str__(self):
        return self.domain