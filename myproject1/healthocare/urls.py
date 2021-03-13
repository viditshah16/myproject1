from django.urls import path
from . import views

urlpatterns = [
    path("index",views.index, name="index"),
    path("index/cart/",views.cart, name="cart"),
    path("index/checkout/",views.checkout, name="checkout"),
    path("index/update_item/",views.updateItem, name="update_item"),
    path("index/process_order/",views.processOrder, name="process_order"),
]
