class StockException(Exception):
    """Exceção base para erros relacionados ao estoque"""
    pass

class InsufficientStockError(StockException):
    """Exceção lançada quando não há estoque suficiente"""
    def __init__(self, product_id: int, available: int, requested: int):
        self.product_id = product_id
        self.available = available
        self.requested = requested
        super().__init__(
            f"Produto {product_id} tem estoque insuficiente. "
            f"Disponível: {available}ml, Solicitado: {requested}ml"
        )

class ProductNotFoundError(StockException):
    """Exceção lançada quando o produto não é encontrado"""
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Produto com id {product_id} não encontrado")

class StockNotFoundError(StockException):
    """Exceção lançada quando não há registro de estoque para o produto"""
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Não há estoque disponível para o produto {product_id}") 