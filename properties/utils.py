from .models import Property
from django.core.cache import cache


def get_all_properties():
    """
    Check the cache for all properties, if not found, fetch from the database.
    """
    
    cached_response = cache.get('all_properties')
    
    if cached_response:
        return cached_response
      
    queryset = Property.objects.all().order_by('created_at')
    
    cache.set('all_properties', queryset, 3600)
    
    return queryset