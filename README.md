# redis-distributed-lock

Python3的redis分布式锁, 使用 setnx 和 lua script, 提供 block 和 no-block 函数

#### 用法

```
import redis

from .redis_lock import RedisLock


redis_conn = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
lock = RedisLock(redis_conn)

lock = RedisLock(redis_conn, sleeptime=100)

lock = RedisLock(redis_conn, prefix='lock')

# 使用 block 模式
key = 'key'
try:
    if lock.acquire(key, expire=3000, timeout=2):
        # TODO
        pass
finally:
    lock.release(key)

# 使用 No-block 模式
lock.acquire_no_block(key)
```
