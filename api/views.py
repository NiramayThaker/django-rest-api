from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from api.models import *
from api.serializers import *

from .filters import InStockFilterBackend, OrderFilter, ProductFilter

# from django.http import JsonResponse, HttpResponse
# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # Have to specify which filters are being used in backend
    filterset_class = ProductFilter
    filter_backends = [
        InStockFilterBackend,
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    # Name must be exact match when used '=' before it
    search_fields = ['=name', 'description']
    ordering_fields = ['name', 'price', 'stock']

    # Adding pagination to specific class not to every data begin loaded
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 2
    # pagination_class.page_query_param = 'pagenum'
    # pagination_class.page_size_query_param = 'size'
    # pagination_class.max_page_size = 6

    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        self.permission_classes = [AllowAny]

        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]

        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()


# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer


# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # Dynamically filtering the query
#         return super().get_queryset().filter(user=self.request.user)

#     # def get_queryset(self):
#     #     user = self.request.user
#     #     qs = super.get_queryset()
#     #     return qs.filter(user=user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # If it is a post request the OrderCreateSerializer is passed
        if self.action == 'create' or self.action == 'update':
            return OrderCreateSerializer
        
        # Or normal serializer class
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)        

        return qs

    # Adding custom logic using action
    # @action(
    #     detail=False,
    #     methods=['get'], 
    #     url_path='user-orders',
    # )
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(orders, many=True)
    #     return Response(serializer.data)


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })

        return Response(serializer.data)
 

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)

#     return Response(serializer.data)


# @api_view(['GET'])
# def get_product(request, pk):
#     product = get_object_or_404(Product, id=pk)
    
#     serializer = ProductSerializer(product)
    
#     return Response(serializer.data)

# @api_view(['GET'])
# def order_list(request):
#     # Featch all the data which is related in one query rather than feaching it for every single item

#     # orders = Order.objects.prefetch_related(
#     #     'items', 'items__product'
#     # ).all()

#     # Both are same as when we featch product from items it automatically featches items 

#     # orders = Order.objects.prefetch_related('items__product').all()
#     orders = Order.objects.prefetch_related('items__product')

#     serializer = OrderSerializer(orders, many=True)

#     return Response(serializer.data)

# @api_view(['GET'])
# def product_info(request):
    # products = Product.objects.all()
    # serializer = ProductInfoSerializer({
    #     'products': products,
    #     'count': len(products),
    #     'max_price': products.aggregate(max_price=Max('price'))['max_price']
    # })

    # return Response(serializer.data)


######################################
# Class Based views
######################################
# class ProductListAPIView(generics.ListAPIView):
#     # queryset = Product.objects.filter(stock__gt=0)
#     # queryset = Product.objects.exclude(stock__gt=0)
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class ProductCreateAPIView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer
