from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, AvailableProductsView, ConsumeStockView

router = DefaultRouter()
router.register('', ProductViewSet)

urlpatterns = [
    path('available-products/', AvailableProductsView.as_view(), name='available-products'),
    path('stock/consume/', ConsumeStockView.as_view(), name='consume-stock'),
    path('', include(router.urls)),
] 