class CacheService:
    def __init__(self):
        self._cache = {}
        
    def set(self, key: str, value: any):
        self._cache[key] = value
        
    def get(self, key: str) -> any:
        return self._cache.get(key)
