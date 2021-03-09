from django.urls import path
from . import views

urlpatterns = [
    path("index",views.index, name="index"),
    path("index/cart/",views.cart, name="cart"),
    path("index/checkout/",views.checkout, name="checkout"),
]
