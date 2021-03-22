# redis-distributed-lock

Python3的redis分布式锁, 使用 setnx 和 lua script, 提供 block 和 no-block 函数

## 官方推荐使用lua脚本确保原子性

```
if redis.call('get', KEYS[1]) == ARGV[1] then
    return redis.call('del', KEYS[1])
else
    return 0
end
```

## 用法

```
import redis

from .redis_lock import RedisLock


redis_client = redis.Redis(host="127.0.0.1", port=6379, db=0)
lock = RedisLock(redis_client)

lock = RedisLock(redis_client, sleeptime=100)

lock = RedisLock(redis_client, prefix='lock')

# 使用 block 模式
lock_name = 'lock_name'
try:
    if lock.acquire(lock_name, expire=3000, acquire_timeout=2):
        # TODO
        pass
finally:
    lock.release(lock_name)

# 使用 No-block 模式
lock.acquire_no_block(lock_name)
```
