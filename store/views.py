from django.db.models.aggregates import Count
from itertools import count, product
from multiprocessing import context
from urllib.robotparser import RequestRate
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializers import CollectionSerializer, ProductSerializer


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            query_set, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('ok ')
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # to avoid the if else we can simple write
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is assosicated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # optimised way
    # product = get_object_or_404(Product, pk=id)
    # serializer = ProductSerializer(product)
    # return Response(serializer.data)

    # default way
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
