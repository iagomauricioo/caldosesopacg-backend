from rest_framework import serializers
from .models import Client, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["id", "client"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        read_only_fields = ["id"]


class ClientDetailSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ["id", "name", "phone", "addresses"]
