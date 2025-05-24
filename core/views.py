from django.urls import get_resolver
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from collections import OrderedDict

@api_view(['GET'])
def api_root(request):
    """
    Lista todas as URLs disponíveis na API.
    """
    urls = OrderedDict()
    
    # URLs da API
    urls['products'] = reverse('product-list', request=request)
    
    # URLs de documentação
    urls['swagger'] = reverse('schema-swagger-ui', request=request)
    urls['redoc'] = reverse('schema-redoc', request=request)
    
    return Response(urls) 