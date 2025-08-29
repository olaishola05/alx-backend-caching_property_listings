from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .utils import get_all_properties

@cache_page(60 * 15)
def property_list(request):
    """
    Returns a list of all properties, with the response cached in Redis for 15 minutes.
    """

    properties = get_all_properties()
    properties_list = [model_to_dict(prop) for prop in properties]

    return JsonResponse({
       'success': True,
       'count': len(properties_list),
       'data': properties_list
   }, status=200)
