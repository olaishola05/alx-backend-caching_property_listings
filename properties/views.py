from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Property
from django.http import JsonResponse
from django.forms.models import model_to_dict

@cache_page(60 * 15)
def property_list(request):
    """
    Returns a list of all properties, with the response cached in Redis for 15 minutes.
    """
    cached_response = cache.get('property_list')
    if cached_response:
        return cached_response
   
    properties = Property.objects.all().order_by('created_at')
    properties_list = [model_to_dict(prop) for prop in properties]

    response = JsonResponse({
        'success': True,
        'count': len(properties_list),
        'properties': properties_list
    }, status=200)

    
    cache.set('property_list', response, timeout=60 * 15)

    return response
