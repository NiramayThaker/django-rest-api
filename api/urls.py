from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # path('orders/', views.OrderListAPIView.as_view()),
    # path('user-orders/', views.UserOrderListAPIView.as_view(), name='user-orders'),
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/info', views.ProductInfoAPIView.as_view()),
    path('product/<str:product_id>', views.ProductDetailAPIView.as_view()),
    path('user', views.UserListView.as_view()),
]

router = DefaultRouter()
router.register('orders', views.OrderViewSet)
urlpatterns += router.urls
