from django.urls import path
from . import views

urlpatterns = [
    path("clients", views.ClientCreateView.as_view()),
    path("clients/", views.ClientListView.as_view()),
    path("clients/<int:pk>", views.ClientDetailView.as_view()),
    path("clients/<int:client_id>/addresses", views.AddressCreateView.as_view()),
    path("clients/<int:client_id>/addresses/", views.AddressListView.as_view()),
]
