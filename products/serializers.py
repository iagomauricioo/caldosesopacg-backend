from rest_framework import serializers
from .models import Product, AvailableProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'prices']
        
    def validate_prices(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("prices must be a list")
            
        for price in value:
            if not isinstance(price, dict):
                raise serializers.ValidationError("each price must be an object")
            if 'size_ml' not in price:
                raise serializers.ValidationError("size_ml is required")
            if 'price_in_cents' not in price:
                raise serializers.ValidationError("price_in_cents is required")
            if not isinstance(price['size_ml'], int):
                raise serializers.ValidationError("size_ml must be an integer")
            if not isinstance(price['price_in_cents'], int):
                raise serializers.ValidationError("price_in_cents must be an integer")
                
        return value

class ProductAvailabilityItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity_in_grams = serializers.IntegerField(min_value=0)

class AvailableProductInputSerializer(serializers.Serializer):
    products = serializers.ListField(
        child=ProductAvailabilityItemSerializer()
    )

class AvailableProductOutputItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    
    class Meta:
        model = AvailableProduct
        fields = ['product_id', 'quantity_in_grams']

class AvailableProductOutputSerializer(serializers.Serializer):
    products = AvailableProductOutputItemSerializer(many=True)

class ConsumeStockItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity_in_grams = serializers.IntegerField(min_value=1)

class ConsumeStockInputSerializer(serializers.Serializer):
    products = serializers.ListField(
        child=ConsumeStockItemSerializer()
    ) 