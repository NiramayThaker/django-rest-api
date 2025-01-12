from django.db.models import Max  
from api.serializers import *
from api.models import *
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView

from .filters import ProductFilter, InStockFilterBackend
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

# from django.http import JsonResponse, HttpResponse
# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view


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


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Dynamically filtering the query
        return super().get_queryset().filter(user=self.request.user)

    # def get_queryset(self):
    #     user = self.request.user
    #     qs = super.get_queryset()
    #     return qs.filter(user=user)


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
