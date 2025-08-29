from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Property
from django.core.cache import cache

@receiver([post_save, post_delete], sender=Property)
def clear_property_cache(sender, **kwargs):
    """
    Clear the property cache when a property is created, updated, or deleted.
    """
    cache.delete('all_properties')