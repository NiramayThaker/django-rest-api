from django.contrib import admin
from .models import Order, OrderItem, Product, User

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(User)
