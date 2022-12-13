from unicodedata import category
from django.db import models
from django.utils import timezone


class keyword_table(models.Model):
   
    keyword = models.TextField(null=True)
    req_url = models.TextField(null=True,blank=True)
    with_year = models.BooleanField(null=True)
    search_volume = models.IntegerField(null=True,blank=True)
    category=models.CharField(max_length=200,blank=True,null=True)
    

    def __str__(self):
        return self.keyword

class rel_search_table(models.Model):
     rel_search=models.TextField(null=True)
     def __str__(self):
        return self.rel_search

class keyword_rel_search_table(models.Model):
    keyword= models.ForeignKey(to=keyword_table,on_delete=models.CASCADE )
    rel_search= models.ForeignKey(to=rel_search_table,on_delete=models.CASCADE )
    date=models.DateField(default=None)

class brand_table(models.Model):
    brand=models.CharField(max_length= 100)
    def __str__(self):
        return self.brand

class keyword_brand_table(models.Model):
    keyword= models.ForeignKey(to=keyword_table,on_delete=models.CASCADE )
    brand= models.ForeignKey(to=brand_table,on_delete=models.CASCADE )
    


class tag_table(models.Model):   
    tag=models.CharField(max_length= 300,null=True) 
    def __str__(self):
        return self.tag

class keyword_tag_table(models.Model):
    keyword= models.ForeignKey(to=keyword_table,on_delete=models.CASCADE )
    tag= models.ForeignKey(to=tag_table,on_delete=models.CASCADE ,null=True)

class frequency_table(models.Model):   
    frequency=models.CharField(max_length= 300,null=True) 
    def __str__(self):
        return self.frequency

class keyword_frequency_table(models.Model):
    keyword= models.ForeignKey(to=keyword_table,on_delete=models.CASCADE )
    frequency= models.ForeignKey(to=frequency_table,on_delete=models.CASCADE ,null=True)
   
    


class domain_table(models.Model):
    domain=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.domain

class rel_question_table(models.Model):
     rel_question= models.TextField(null=True)
     pos=models.IntegerField(null=True)
     answer=models.TextField(null=True)
     source_url = models.TextField(null=True)
     source_title=models.TextField(null=True)
     domain=models.ForeignKey(to=domain_table,on_delete=models.CASCADE )
     url_shown = models.TextField(null=True)

     def __str__(self):
        return self.rel_question
class keyword_rel_question_table(models.Model):
    keyword= models.ForeignKey(to=keyword_table,on_delete=models.CASCADE )
    question= models.ForeignKey(to=rel_question_table,on_delete=models.CASCADE )
    date=models.DateField(default=None)

class description_table(models.Model):
    desc_id = models.TextField(primary_key=True)
    keyword= models.ForeignKey(to=keyword_table,on_delete=models.CASCADE )
    url = models.TextField(null=True,blank=True)
    date=models.DateField(blank=True,null=True)
    pos=models.IntegerField()
    domain=models.ForeignKey(to=domain_table,on_delete=models.CASCADE )
    title = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,
    blank=True)    
    pos_overall = models.IntegerField(null=True,blank=True)
    url_shown = models.TextField(null=True,blank=True)

    def save(self, *args, **kwargs):
        self.desc_id = self.keyword + self.domain + self.date+self.pos
        super(description_table, self).save(*args, **kwargs)
    def __str__(self):
        # return '{} {} {} {} {} {} '.format(self.desc_id,self.keyword,self.url,self.pos,self.domain,self.date)
        return self.desc_id

class sitelink_table(models.Model):
    desc=models.ForeignKey(to=description_table,to_field='desc_id', on_delete=models.CASCADE )
    url_type = models.CharField(max_length=50,null=True,blank=True)
    url = models.TextField(null=True)
    title= models.TextField(null=True)

    def __str__(self):
        return self.url

class question_table(models.Model):
    desc=models.ForeignKey(to=description_table,to_field='desc_id', on_delete=models.CASCADE )
    question=models.TextField(null=True,blank=True)
    pos=models.IntegerField()

    def __str__(self):
        return self.question
