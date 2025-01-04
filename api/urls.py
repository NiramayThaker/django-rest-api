from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('product/<str:pk>', views.get_product),
    path('orders/', views.order_list),
]
