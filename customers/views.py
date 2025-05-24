from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Client
from .serializers import ClientSerializer, ClientDetailSerializer, AddressSerializer


# Create a client
class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# List all clients
class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# Retrieve client with addresses
class ClientDetailView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer


# Create address for a client
class AddressCreateView(APIView):
    def post(self, request, client_id):
        client = generics.get_object_or_404(Client, pk=client_id)
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=client)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# List addresses of a client
class AddressListView(APIView):
    def get(self, request, client_id):
        client = generics.get_object_or_404(Client, pk=client_id)
        addresses = client.addresses.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
