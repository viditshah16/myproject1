from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Best_Deals)
admin.site.register(Diagnostic_Packages)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)