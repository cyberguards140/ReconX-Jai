import asyncio
import logging

import aiohttp

from core.models.cloud import CloudAsset

logger = logging.getLogger(__name__)


class S3BucketScanner:
    """
    Identifies misconfigured public S3 buckets via permutations and direct DNS probing.
    """

    def __init__(self):
        # A small MVP permutation list
        self.permutations = ["", "-dev", "-prod", "-staging", "-test", "-assets", "-public"]

    async def _check_bucket_public(
        self, session: aiohttp.ClientSession, bucket_name: str
    ) -> CloudAsset | None:
        url = f"https://{bucket_name}.s3.amazonaws.com"
        try:
            async with session.get(url, timeout=3) as response:
                if response.status in [200, 403]:
                    # 200 = Listable (highly vulnerable)
                    # 403 = Exists but not listable (still an asset)
                    is_public = response.status == 200
                    return CloudAsset(
                        provider="aws",
                        service_type="s3_bucket",
                        identifier=bucket_name,
                        is_public=is_public,
                        metadata={"status_code": response.status, "url": url},
                        sources=["s3_scanner"],
                    )
        except Exception:
            pass
        return None

    async def scan(self, base_keyword: str) -> list[CloudAsset]:
        """
        Scans for buckets using the base keyword and permutations.
        """
        logger.info(f"Scanning S3 buckets for keyword: {base_keyword}")
        found_assets = []
        async with aiohttp.ClientSession() as session:
            tasks = []
            for perm in self.permutations:
                # e.g., company-dev
                tasks.append(self._check_bucket_public(session, f"{base_keyword}{perm}"))

            results = await asyncio.gather(*tasks)
            for r in results:
                if r:
                    found_assets.append(r)

        return found_assets


s3_scanner = S3BucketScanner()
