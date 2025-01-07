from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view()),
    path('products/info', views.product_info),
    path('product/<str:product_id>', views.ProductDetailAPIView.as_view()),
    path('orders/', views.order_list),
]
