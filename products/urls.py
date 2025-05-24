from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, AvailableProductsView

router = DefaultRouter()
router.register('', ProductViewSet)

urlpatterns = [
    path('available-products/', AvailableProductsView.as_view(), name='available-products'),
    path('', include(router.urls)),
] 