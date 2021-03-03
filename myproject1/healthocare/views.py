from django.shortcuts import render
from .models import Best_Deals, Diagnostic_Packages

# Create your views here.

def index(request):
    
    #below three bds are used to set static content
    #bd1 = Best_Deals()
    #bd1.img = '11.jfif'
    #bd1.name = 'VLCC Sunscream'
    #bd1.desc = 'Suncream is best for body'
    #bd1.mfr = 'VLCC PVT. LTD.'
    #bd1.price = 395.00
    #bd1.offer = 15
    #bd1.offer_price = 335.75
    
    #bd2 = Best_Deals()
    #bd2.img = '12.jfif'
    #bd2.name = 'LA shield Sunscream'
    #bd2.desc = 'best sunscream in india'
    #bd2.mfr = 'GLENMARK PHARMACEUTICALS LTD.'
    #bd2.price = 920.00
    #bd2.offer = 13
    #bd2.offer_price = 800.40
    
    #bd3 = Best_Deals()
    #bd3.img = '13.jfif'
    #bd3.name = 'Sri Sri Sunscream'
    #bd3.desc = 'best sunscream in the world'
    #bd3.mfr = 'SRIVEDA SATVA PVT. LTD.'
    #bd3.price = 80.00
    #bd3.offer = 5
    #bd3.offer_price = 76.00
    
    #bds = [ bd1, bd2, bd3 ]
    
    #now using dynamic data from the database
    bds = Best_Deals.objects.all()
    dps = Diagnostic_Packages.objects.all()
    
    return render(request, 'index.html', {'bds': bds, 'dps': dps})