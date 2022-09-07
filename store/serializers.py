from dataclasses import field
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection, Review

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Collection
        fields = ['id', 'title', 'products_count']
    products_count = serializers.IntegerField(read_only=True)
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)

    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection',]
    # we can use diff variable name but should specify source to look for in model
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # description = serializers.CharField(null=True, blank=True)
    # slug = serializers.SlugField()
    # inventory = serializers.IntegerField(validators=[MinValueValidator(0)])
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')   
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = CollectionSerializer() 
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail')
    
    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description', 'product']
        read_only_fields = ('product',)

    def create(self, validated_data):
        product_id = self.context['product_id']
        Review.objects.create(product_id=product_id, **validated_data) 