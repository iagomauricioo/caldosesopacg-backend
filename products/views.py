from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from .models import Product, AvailableProduct
from .serializers import (
    ProductSerializer, 
    AvailableProductInputSerializer,
    AvailableProductOutputSerializer,
    ConsumeStockInputSerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def create(self, request, *args, **kwargs):
        # Verifica se é uma lista ou um único objeto
        is_many = isinstance(request.data, list)
        
        if is_many:
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
            
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

@method_decorator(csrf_exempt, name='dispatch')
class AvailableProductsView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post']  # Explicitamente permitindo GET e POST
    
    @swagger_auto_schema(
        operation_description="Get all available products for today",
        responses={
            200: AvailableProductOutputSerializer,
            500: openapi.Response(
                description="Internal Server Error",
                examples={
                    "application/json": {
                        "error": {
                            "type": "internal_error",
                            "message": "An unexpected error occurred",
                            "details": "Error details here"
                        }
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        # Pegar a data atual
        today = timezone.now().date()
        
        # Buscar produtos disponíveis
        available_products = AvailableProduct.objects.filter(
            date=today,
            quantity_in_ml__gt=0
        ).select_related('product')
        
        # Serializar resposta
        serializer = AvailableProductOutputSerializer({"products": list(available_products)})
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update product availability for today",
        request_body=AvailableProductInputSerializer,
        responses={
            200: AvailableProductOutputSerializer,
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": {
                            "type": "validation_error",
                            "message": "Invalid input data",
                            "details": {
                                "products": ["This field is required"]
                            }
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": {
                            "type": "not_found",
                            "message": "Product not found",
                            "details": None
                        }
                    }
                }
            ),
            500: openapi.Response(
                description="Internal Server Error",
                examples={
                    "application/json": {
                        "error": {
                            "type": "internal_error",
                            "message": "An unexpected error occurred",
                            "details": "Error details here"
                        }
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        # Validar input
        input_serializer = AvailableProductInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        
        # Pegar a data atual
        today = timezone.now().date()
        
        # Criar ou atualizar disponibilidades
        available_products = []
        for product in input_serializer.validated_data['products']:
            # Verificar se o produto existe
            try:
                product_obj = Product.objects.get(id=product['product_id'])
            except Product.DoesNotExist:
                raise ObjectDoesNotExist(f"Product with id {product['product_id']} does not exist")
                
            available_product, _ = AvailableProduct.objects.update_or_create(
                product=product_obj,
                date=today,
                defaults={'quantity_in_ml': product['quantity_in_ml']}
            )
            available_products.append(available_product)
        
        # Serializar resposta
        serializer = AvailableProductOutputSerializer({"products": available_products})
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class ConsumeStockView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Consume stock from available products",
        request_body=ConsumeStockInputSerializer,
        responses={
            200: AvailableProductOutputSerializer,
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": {
                            "type": "validation_error",
                            "message": "Invalid input data",
                            "details": {
                                "products": ["This field is required"]
                            }
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": {
                            "type": "not_found",
                            "message": "Product not found",
                            "details": None
                        }
                    }
                }
            ),
            422: openapi.Response(
                description="Unprocessable Entity",
                examples={
                    "application/json": {
                        "error": {
                            "type": "validation_error",
                            "message": "Insufficient stock",
                            "details": "Product 1 has insufficient stock. Available: 100g, Requested: 300g"
                        }
                    }
                }
            )
        }
    )
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Validar input
        input_serializer = ConsumeStockInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        
        today = timezone.now().date()
        updated_products = []
        
        # Verificar e atualizar cada produto
        for product_data in input_serializer.validated_data['products']:
            try:
                available_product = AvailableProduct.objects.select_for_update().get(
                    product_id=product_data['product_id'],
                    date=today
                )
                
                # Verificar se há estoque suficiente
                if available_product.quantity_in_ml < product_data['quantity_in_ml']:
                    raise serializers.ValidationError({
                        "error": {
                            "type": "validation_error",
                            "message": "Insufficient stock",
                            "details": f"Product {product_data['product_id']} has insufficient stock. "
                                     f"Available: {available_product.quantity_in_ml}ml, "
                                     f"Requested: {product_data['quantity_in_ml']}ml"
                        }
                    })
                
                # Atualizar o estoque
                available_product.quantity_in_ml -= product_data['quantity_in_ml']
                available_product.save()
                updated_products.append(available_product)
                
            except AvailableProduct.DoesNotExist:
                raise ObjectDoesNotExist(
                    f"No available stock found for product {product_data['product_id']}"
                )
        
        # Serializar resposta
        serializer = AvailableProductOutputSerializer({"products": updated_products})
        return Response(serializer.data, status=status.HTTP_200_OK)
