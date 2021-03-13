from django.db import models
from django.contrib.auth.models import User
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
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) 
    # we have set on_delete to null as when customer gets deleted we don't want to delete the order we just want to set customer value to null
    date_ordered = models.DateTimeField(auto_now_add=True)
    # auto_now_add field saves the current timestamp when a row is first added to the database, and is therefore perfect for tracking when it was created.
    complete = models.BooleanField(default=False, null=True, blank=False) # To indicate order status
    transaction_id = models.CharField(max_length=255, null=True)
   
    def __str__(self):
        return str(self.id)
       
    @property
    def get_cart_total(self): # to get total amount of the whole cart
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self): # to get total item quantity in the cart
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property 
    def shipping(self):
        shipping = True
        orderitems = self.orderitem_set.all()
        return shipping
    
    # since we are adding the "shipping" method tot our order we can use it in the template straight away 
    # by accessing it like any other property
    
class OrderItem(models.Model):
    product = models.ForeignKey(Best_Deals, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self): # it is used to get total amount for the given product in cart
        total = self.product.offer_price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length = 1000)
    city = models.CharField(max_length = 255)
    state = models.CharField(max_length = 255)
    country = models.CharField(max_length = 255)
    zip_code = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address