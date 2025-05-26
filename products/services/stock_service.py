from typing import List, Dict
from django.utils import timezone
from django.db import transaction
from ..models import Product, AvailableProduct
from ..exceptions.stock_exceptions import (
    InsufficientStockError,
    ProductNotFoundError,
    StockNotFoundError
)

class StockService:
    @staticmethod
    def get_available_products() -> List[AvailableProduct]:
        """Retorna todos os produtos disponíveis para hoje"""
        today = timezone.now().date()
        return AvailableProduct.objects.filter(
            date=today,
            quantity_in_ml__gt=0
        ).select_related('product')

    @staticmethod
    def update_availability(products_data: List[Dict]) -> List[AvailableProduct]:
        """Atualiza a disponibilidade dos produtos para hoje"""
        today = timezone.now().date()
        available_products = []

        for product_data in products_data:
            try:
                product = Product.objects.get(id=product_data['product_id'])
            except Product.DoesNotExist:
                raise ProductNotFoundError(product_data['product_id'])

            available_product, _ = AvailableProduct.objects.update_or_create(
                product=product,
                date=today,
                defaults={'quantity_in_ml': product_data['quantity_in_ml']}
            )
            available_products.append(available_product)

        return available_products

    @staticmethod
    @transaction.atomic
    def consume_stock(products_data: List[Dict]) -> List[AvailableProduct]:
        """Consome estoque dos produtos disponíveis"""
        today = timezone.now().date()
        updated_products = []

        for product_data in products_data:
            try:
                available_product = AvailableProduct.objects.select_for_update().get(
                    product_id=product_data['product_id'],
                    date=today
                )
            except AvailableProduct.DoesNotExist:
                raise StockNotFoundError(product_data['product_id'])

            if available_product.quantity_in_ml < product_data['quantity_in_ml']:
                raise InsufficientStockError(
                    product_data['product_id'],
                    available_product.quantity_in_ml,
                    product_data['quantity_in_ml']
                )

            available_product.quantity_in_ml -= product_data['quantity_in_ml']
            available_product.save()
            updated_products.append(available_product)

        return updated_products 