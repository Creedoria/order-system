import redis.asyncio as Redis

redis_client: Redis.Redis | None = None

def get_redis() -> Redis.Redis:
    if redis_client is None:
        raise RuntimeError("Redis client not initialized")
    return redis_client