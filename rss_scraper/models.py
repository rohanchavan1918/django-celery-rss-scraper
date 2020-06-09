from django.db import models

# Create your models here.

class ScrapedData(models.Model):
    Title = models.CharField(max_length=150,null=False)
    Description = models.CharField(max_length=500,null=False)
    Date = models.DateField(auto_now=False,null=False)
    url = models.URLField(max_length=500,null=False)
    
    def __str__(self):
        return self.Title
