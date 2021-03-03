from django.db import models

# Create your models here.

class Best_Deals(models.Model):
    #This below code is used for static data change
    #img: str
    #name: str
    #desc: str
    #mfr: str
    #price: float
    #offer: float
    #offer_price: float
    
    #This below code is used for dynamic data change i.e., from database using tables
    img = models.ImageField(upload_to='pics')
    name = models.CharField(max_length = 1000)
    desc = models.TextField()
    mfr = models.CharField(max_length = 5000)
    price = models.FloatField()
    offer = models.IntegerField()
    offer_price = models.FloatField()
    
class Diagnostic_Packages(models.Model):
    img = models.ImageField(upload_to='pics')
    name = models.CharField(max_length = 1000)
    desc = models.TextField()
    price = models.FloatField()