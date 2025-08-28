from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Property

@cache_page(60 * 15)
def property_list(request):
    """
    Returns a list of all properties, with the response cached in Redis for 15 minutes.
    """
    # This code will only execute if the page is not in the cache or has expired.
    properties = Property.objects.all().order_by('created_at')
    
    context = {
        'properties': properties
    }
    return render(request, 'properties/property_list.html', context)
