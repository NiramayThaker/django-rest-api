from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Max  
from api.serializers import *
from api.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics


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


class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.filter(stock__gt=0)
    # queryset = Product.objects.exclude(stock__gt=0)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'




@api_view(['GET'])
def order_list(request):
    # Featch all the data which is related in one query rather than feaching it for every single item

    # orders = Order.objects.prefetch_related(
    #     'items', 'items__product'
    # ).all()

    # Both are same as when we featch product from items it automatically featches items 

    # orders = Order.objects.prefetch_related('items__product').all()
    orders = Order.objects.prefetch_related('items__product')

    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })

    return Response(serializer.data)
