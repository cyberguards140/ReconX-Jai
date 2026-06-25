class Deduplicator:
    def is_duplicate(self, asset_type, value):
        # AssetManager already handles DB-level dedup, this can be used for in-memory stream dedup
        pass
