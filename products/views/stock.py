from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..serializers.stock import (
    AvailableProductInputSerializer,
    AvailableProductOutputSerializer,
    ConsumeStockInputSerializer
)
from ..services.stock_service import StockService
from ..exceptions.stock_exceptions import (
    StockException,
    InsufficientStockError,
    ProductNotFoundError,
    StockNotFoundError
)

@method_decorator(csrf_exempt, name='dispatch')
class AvailableProductsView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        operation_description="Obter todos os produtos disponíveis para hoje",
        responses={
            200: AvailableProductOutputSerializer,
            500: openapi.Response(
                description="Erro Interno do Servidor",
                examples={
                    "application/json": {
                        "error": {
                            "type": "internal_error",
                            "message": "Ocorreu um erro inesperado",
                            "details": "Detalhes do erro aqui"
                        }
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            available_products = StockService.get_available_products()
            serializer = AvailableProductOutputSerializer({"products": list(available_products)})
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {
                    "error": {
                        "type": "internal_error",
                        "message": "Ocorreu um erro inesperado",
                        "details": str(e)
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Atualizar disponibilidade dos produtos para hoje",
        request_body=AvailableProductInputSerializer,
        responses={
            200: AvailableProductOutputSerializer,
            400: openapi.Response(description="Dados inválidos"),
            404: openapi.Response(description="Produto não encontrado"),
            500: openapi.Response(description="Erro Interno do Servidor")
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            input_serializer = AvailableProductInputSerializer(data=request.data)
            input_serializer.is_valid(raise_exception=True)
            
            available_products = StockService.update_availability(
                input_serializer.validated_data['products']
            )
            
            serializer = AvailableProductOutputSerializer({"products": available_products})
            return Response(serializer.data)
            
        except ProductNotFoundError as e:
            return Response(
                {
                    "error": {
                        "type": "not_found",
                        "message": str(e),
                        "details": None
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "error": {
                        "type": "internal_error",
                        "message": "Ocorreu um erro inesperado",
                        "details": str(e)
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_exempt, name='dispatch')
class ConsumeStockView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Consumir estoque dos produtos disponíveis",
        request_body=ConsumeStockInputSerializer,
        responses={
            200: AvailableProductOutputSerializer,
            400: openapi.Response(description="Dados inválidos"),
            404: openapi.Response(description="Produto ou estoque não encontrado"),
            422: openapi.Response(description="Estoque insuficiente"),
            500: openapi.Response(description="Erro Interno do Servidor")
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            input_serializer = ConsumeStockInputSerializer(data=request.data)
            input_serializer.is_valid(raise_exception=True)
            
            updated_products = StockService.consume_stock(
                input_serializer.validated_data['products']
            )
            
            serializer = AvailableProductOutputSerializer({"products": updated_products})
            return Response(serializer.data)
            
        except (ProductNotFoundError, StockNotFoundError) as e:
            return Response(
                {
                    "error": {
                        "type": "not_found",
                        "message": str(e),
                        "details": None
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except InsufficientStockError as e:
            return Response(
                {
                    "error": {
                        "type": "validation_error",
                        "message": "Estoque insuficiente",
                        "details": str(e)
                    }
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except Exception as e:
            return Response(
                {
                    "error": {
                        "type": "internal_error",
                        "message": "Ocorreu um erro inesperado",
                        "details": str(e)
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 