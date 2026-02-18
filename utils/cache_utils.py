# Create utils/cache_utils.py
import hashlib
import json
from functools import wraps

from django.conf import settings
from django.core.cache import cache


class CacheManager:
    """Advanced cache management utility"""

    @staticmethod
    def get_cache_key(prefix, *args, **kwargs):
        """Generate consistent cache key"""
        key_parts = [prefix]

        # Add args to key
        for arg in args:
            key_parts.append(str(arg))

        # Add kwargs to key (sorted for consistency)
        for key in sorted(kwargs.keys()):
            key_parts.append(f"{key}:{kwargs[key]}")

        # Create hash
        key_string = ":".join(key_parts)
        return f"{settings.CACHES['default']['KEY_PREFIX']}:{hashlib.md5(key_string.encode()).hexdigest()}"

    @staticmethod
    def cached(timeout=None, key_prefix=None):
        """Decorator for caching function results"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                prefix = key_prefix or func.__name__
                cache_key = CacheManager.get_cache_key(prefix, *args, **kwargs)

                # Try to get from cache
                cached_result = cache.get(cache_key)
                if cached_result is not None:
                    return cached_result

                # Execute function
                result = func(*args, **kwargs)

                # Store in cache
                cache.set(
                    cache_key,
                    result,
                    timeout or settings.CACHE_TIMEOUTS.get(prefix, 300),
                )

                return result

            return wrapper

        return decorator

    @staticmethod
    def invalidate_pattern(pattern):
        """Invalidate cache keys matching pattern"""
        # Note: This requires Redis for pattern matching
        # For locmem cache, we can't do pattern matching
        try:
            if hasattr(cache, "delete_pattern"):  # django-redis
                cache.delete_pattern(f"{settings.CACHES['default']['KEY_PREFIX']}:{pattern}*")
        except:
            pass  # Skip if pattern deletion not supported


# Create view cache decorators
from django.views.decorators.cache import cache_page


class ViewCache:
    """View-level caching utilities"""

    @staticmethod
    def cache_public_page(timeout=300):
        """Cache decorator for public pages"""
        return cache_page(timeout, cache="default", key_prefix="public_pages")

    @staticmethod
    def cache_user_page(timeout=60):
        """Cache decorator for user-specific pages"""

        def decorator(view_func):
            @wraps(view_func)
            def wrapper(request, *args, **kwargs):
                # Add user ID to cache key for user-specific caching
                cache_key = f"user_{request.user.id if request.user.is_authenticated else 'anonymous'}"
                return cache_page(timeout, key_prefix=cache_key)(view_func)(request, *args, **kwargs)

            return wrapper

        return decorator
