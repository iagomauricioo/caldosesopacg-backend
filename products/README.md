# Essa API deve retornar os produtos do restaurante

`GET /products`

```JSON
[
  {
    "id": 1,
    "name": "Caldo de Feijão",
    "description": "Caldo caseiro de feijão com tempero especial.",
    "prices": [
      { "size_ml": 300, "price_in_cents": 1200 },
      { "size_ml": 500, "price_in_cents": 1800 }
    ]
  },
  {
    "id": 2,
    "name": "Caldo de Frango",
    "description": "Caldo caseiro de frango com tempero especial.",
    "prices": [
      { "size_ml": 300, "price_in_cents": 1400 },
      { "size_ml": 500, "price_in_cents": 1800 }
    ]
  }
]

```