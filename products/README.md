# Documentação dos Serializers

Este documento descreve a estrutura e funcionamento dos serializers utilizados no projeto para gerenciamento de produtos.

## Estrutura dos Serializers

### 1. ProductSerializer
Serializer responsável pela serialização do modelo `Product`.

**Campos:**
- `id`: Identificador único do produto
- `name`: Nome do produto
- `description`: Descrição do produto
- `prices`: Lista de preços com diferentes tamanhos

**Validações:**
- `prices` deve ser uma lista
- Cada item em `prices` deve ser um objeto com:
  - `size_ml`: Tamanho em mililitros (número inteiro)
  - `price_in_cents`: Preço em centavos (número inteiro)

### 2. ProductAvailabilityItemSerializer
Serializer para itens individuais de disponibilidade de produto.

**Campos:**
- `product_id`: ID do produto (número inteiro)
- `quantity_in_ml`: Quantidade disponível em mililitros (número inteiro não negativo)

### 3. AvailableProductInputSerializer
Serializer para entrada de dados de disponibilidade de produtos.

**Campos:**
- `products`: Lista de `ProductAvailabilityItemSerializer`

### 4. AvailableProductOutputItemSerializer
Serializer para saída de dados de produtos disponíveis.

**Campos:**
- `product_id`: ID do produto (mapeado de `product.id`)
- `quantity_in_grams`: Quantidade disponível em gramas

### 5. AvailableProductOutputSerializer
Serializer para a saída final da lista de produtos disponíveis.

**Campos:**
- `products`: Lista de `AvailableProductOutputItemSerializer`

### 6. ConsumeStockItemSerializer
Serializer para itens individuais de consumo de estoque.

**Campos:**
- `product_id`: ID do produto (número inteiro)
- `quantity_in_ml`: Quantidade a ser consumida em mililitros (número inteiro positivo, mínimo 1)

### 7. ConsumeStockInputSerializer
Serializer para entrada de dados de consumo de estoque.

**Campos:**
- `products`: Lista de `ConsumeStockItemSerializer`

## Uso

### Exemplo de Dados de Entrada para ProductSerializer
```json
{
  "name": "Produto Exemplo",
  "description": "Descrição do produto",
  "prices": [
    {
      "size_ml": 500,
      "price_in_cents": 1000
    },
    {
      "size_ml": 1000,
      "price_in_cents": 1800
    }
  ]
}
```

### Exemplo de Dados de Entrada para ConsumeStockInputSerializer
```json
{
  "products": [
    {
      "product_id": 1,
      "quantity_in_ml": 500
    },
    {
      "product_id": 2,
      "quantity_in_ml": 1000
    }
  ]
}
```

## Observações Importantes

1. Todos os campos numéricos são validados para garantir que sejam números inteiros
2. Quantidades em mililitros não podem ser negativas
3. Para consumo de estoque, a quantidade mínima é 1 ml
4. Os preços são sempre armazenados em centavos para evitar problemas com números decimais 