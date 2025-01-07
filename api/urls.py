from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.OrderListAPIView.as_view()),
    path('products/', views.ProductListAPIView.as_view()),
    path('products/info', views.product_info),
    path('product/<str:pk>', views.ProductDetailAPIView.as_view()),
]
