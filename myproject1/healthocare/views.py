from django.shortcuts import render
from django.contrib.auth.models import User, auth
from .models import *
from django.http import JsonResponse
import json
import datetime

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
    
    if request.user.is_authenticated: # if user is authenticated / logged in then set its cart value
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False) # complete = False as it is open order/cart
        # here we want to either create an order or get it if they exists
        items = order.orderitem_set.all()
        # we are able to query child object (i.e., orderitem) by setting their parent value (i.e., order)
        # so its set all orderitem that have order as their parent
        cartItems = order.get_cart_items
    else: # if user is not authenticated / not logged in then set items to empty and cart_item and cart_total to zero
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0, 'shipping':False} # setting cart_total & cart_item to 0 and shipping to False if user isn't logged in
        cartItems = order['get_cart_items']
    
    #now using dynamic data from the database
    bds = Best_Deals.objects.all()
    dps = Diagnostic_Packages.objects.all()
    
    return render(request, 'index.html', {'bds': bds, 'dps': dps, 'cartItems': cartItems})
    
def cart(request):
    if request.user.is_authenticated: # if user is authenticated / logged in then set its cart value
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False) # complete = False as it is open order/cart
        # here we want to either create an order or get it if they exists
        items = order.orderitem_set.all()
        # we are able to query child object (i.e., orderitem) by setting their parent value (i.e., order)
        # so its set all orderitem that have order as their parent
        cartItems = order.get_cart_items
    else: # if user is not authenticated / not logged in then set items to empty and cart_item and cart_totak to zero
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0, 'shipping':False} # setting cart_total & cart_item to 0 and shipping to False if user isn't logged in
        cartItems = order['get_cart_items']
    return render(request, 'cart.html', {'items': items, 'order':order, 'cartItems': cartItems})
    
def checkout(request):
    if request.user.is_authenticated: # if user is authenticated / logged in then set its cart value
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False) # complete = False as it is open order/cart
        # here we want to either create an order or get it if they exists
        items = order.orderitem_set.all()
        # we are able to query child object (i.e., orderitem) by setting their parent value (i.e., order)
        # so its set all orderitem that have order as their parent
        cartItems = order.get_cart_items
    else: # if user is not authenticated / not logged in then set items to empty and cart_item and cart_totak to zero
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0, 'shipping':False} # setting cart_total & cart_item to 0 and shipping to False if user isn't logged in
        cartItems = order['get_cart_items']
    return render(request, 'checkout.html', {'items': items, 'order':order, 'cartItems': cartItems})

def updateItem(request): # updateItem function
    # print(request.POST)
    
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('productId:',productId)
    print('action:',action)
    
    customer = request.user
    product = Best_Deals.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # setting the order and product value to the values we have above. The reason why we use 
    # get_or_create is because later in the cart page we want to have the ability to update the 
    # quantity of an order with the "add" action instead of creating a new one every time.
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    # the reason why i have used get_or_create is because i have to change the value of the order
    # if it already exist so if this order item already exist according to the product and the order
    # i don't want to create a newone i will just change the quantity of it so we can add or subtract
    
    if action == 'add': # if action is add then add an item
        msg = 'Item was added'
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove': # else if action is remove then remove an item
        msg = 'Item was removed'
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save() # and then save it
    
    if orderItem.quantity <= 0: # if item quantity is less than or equal to zero then delete an item from the cart
        orderItem.delete()
        
    if action == 'add':
        return JsonResponse(msg, safe=False)
    elif action == 'remove':
        return JsonResponse(msg, safe=False)
    # If safe is set to False any object can be passed for serialization otherwise only dict instances are allowed.

def processOrder(request):
    print('data:',request.body)
    transaction_id = datetime.datetime.now().timestamp() # setting transaction_id
    # to create transaction_id i am using time stamp only
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
        # because i am sending the total from the frontend, i am making sure that the total sent
        # matches with the cart total which is actually supposed to be
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            country = data['shipping']['country'],
            zip_code = data['shipping']['zip_code']
            # in ShippingAddress of models.py there is also a column name date_added but it is set automatically so we don't need to set it here
            )
    else:
        print("user is not logged in")
    return JsonResponse('Payment complete!', safe=False)
    
def payment_success(request):
    return render(request, 'payment_success.html')