from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from products.models import Product, AvailableProduct

class ProductModelTest(TestCase):
    def setUp(self):
        self.product_data = {
            "name": "Test Product",
            "description": "Test Description",
            "prices": [{"size_ml": 1000, "price_in_cents": 1800}]
        }
        self.product = Product.objects.create(**self.product_data)

    def test_criacao_de_produtos_deve_manter_valores_originais(self):
        """Testa se os valores são mantidos após a criação do produto"""
        self.assertEqual(self.product.name, self.product_data["name"])
        self.assertEqual(self.product.description, self.product_data["description"])
        self.assertEqual(self.product.prices, self.product_data["prices"])

    def test_str_representation(self):
        """Testa se a representação string do produto está correta"""
        self.assertEqual(str(self.product), "Test Product")

    def test_prices_deve_ser_lista_por_padrao(self):
        """Testa se o campo prices é inicializado como lista vazia por padrão"""
        product = Product.objects.create(name="Test", description="Test")
        self.assertEqual(product.prices, [])

    def test_name_nao_pode_ser_vazio(self):
        """Testa se não é possível criar produto com nome vazio"""
        with self.assertRaises(ValidationError):
            product = Product(name="", description="Test")
            product.full_clean()

class AvailableProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            prices=[{"size_ml": 1000, "price_in_cents": 1800}]
        )
        self.available_product_data = {
            "product": self.product,
            "quantity_in_grams": 1000,
            "date": timezone.now().date()
        }
        self.available_product = AvailableProduct.objects.create(**self.available_product_data)

    def test_criacao_de_produtos_disponiveis_deve_manter_valores_originais(self):
        """Testa se os valores são mantidos após a criação da disponibilidade"""
        self.assertEqual(self.available_product.product, self.available_product_data["product"])
        self.assertEqual(self.available_product.quantity_in_grams, self.available_product_data["quantity_in_grams"])
        self.assertEqual(self.available_product.date, self.available_product_data["date"])

    def test_str_representation(self):
        """Testa se a representação string da disponibilidade está correta"""
        expected = f"{self.product.name} - 1000g"
        self.assertEqual(str(self.available_product), expected)

    def test_unique_together_constraint(self):
        """Testa se não é possível criar duas disponibilidades para o mesmo produto na mesma data"""
        with self.assertRaises(IntegrityError):
            AvailableProduct.objects.create(
                product=self.product,
                quantity_in_grams=500,
                date=self.available_product.date
            )

    def test_quantidade_nao_pode_ser_negativa(self):
        """Testa se não é possível criar disponibilidade com quantidade negativa"""
        with self.assertRaises(ValidationError):
            available_product = AvailableProduct(
                product=self.product,
                quantity_in_grams=-1,
                date=timezone.now().date()
            )
            available_product.full_clean()

    def test_produto_required(self):
        """Testa se o campo produto é obrigatório"""
        with self.assertRaises(IntegrityError):
            AvailableProduct.objects.create(
                quantity_in_grams=1000,
                date=timezone.now().date()
            )

    def test_cascade_delete(self):
        """Testa se a disponibilidade é deletada quando o produto é deletado"""
        self.product.delete()
        self.assertEqual(AvailableProduct.objects.filter(id=self.available_product.id).count(), 0)