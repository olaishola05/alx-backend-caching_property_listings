from .models import Property
from django.core.cache import cache
import logging
from django_redis import get_redis_connection
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
  
def get_redis_cache_metrics():
  """
    Connects to Redis, retrieves keyspace hit/miss metrics,
    calculates the hit ratio, logs it, and returns the metrics as a dictionary.
  """
  try:
    conn = get_redis_connection("default")
    info = conn.info('stats')
    
    keyspace_hits = info.get('keyspace_hits', 0)
    keyspace_misses = info.get('keyspace_misses', 0)

    total_requests = keyspace_hits + keyspace_misses
    hit_ratio = (keyspace_hits / total_requests) * 100.0 if total_requests > 0 else 0.0

    metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 2)
        }
  
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    log_message = (
        f"{timestamp} - Redis Cache Metrics: "
        f"Hits={metrics['keyspace_hits']}, Misses={metrics['keyspace_misses']}, "
        f"Total={metrics['total_requests']}, Hit Ratio={metrics['hit_ratio']:.2f}%"
    )
    logger.info(log_message)

    return metrics
    # else:
    return {
        'keyspace_hits': 0,
        'keyspace_misses': 0,
        'total_requests': 0,
        'hit_ratio': 0.0,
    }
  except Exception as e:
    error_message = f"Error fetching Redis cache metrics: {e}"
    logger.error(error_message)
    return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0.0,
            'error': error_message
        }