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

## 测试

```
cd redis-distributed-lock
pipenv --python /usr/local/python3.8/bin/python3
pipenv shell
pipenv install
(env) $ python test.py
线程[6]--获得了锁
线程[6]--抢到一张票，还剩9张票
线程[12]--获得了锁
线程[12]--抢到一张票，还剩8张票
线程[6]--获得了锁
线程[12]--获得了锁
线程[7]--获得了锁
线程[7]--抢到一张票，还剩7张票
线程[7]--获得了锁
线程[22]--获得了锁
线程[22]--抢到一张票，还剩6张票
线程[22]--获得了锁
线程[68]--获得了锁
线程[68]--抢到一张票，还剩5张票
线程[48]--获得了锁
线程[68]--获得了锁
线程[48]--抢到一张票，还剩4张票
线程[76]--获得了锁
线程[76]--抢到一张票，还剩3张票
线程[70]--获得了锁
线程[70]--抢到一张票，还剩2张票
线程[94]--获得了锁
线程[94]--抢到一张票，还剩1张票
线程[48]--获得了锁
线程[94]--获得了锁
线程[70]--获得了锁
线程[76]--获得了锁
线程[90]--获得了锁
线程[90]--抢到一张票，还剩0张票
线程[90]--获得了锁
线程[27]--获得了锁
线程[27]--没抢到，票抢完了
线程[77]--获得了锁
线程[77]--没抢到，票抢完了
线程[52]--获得了锁
线程[52]--没抢到，票抢完了
线程[13]--获得了锁
线程[13]--没抢到，票抢完了
线程[28]--获得了锁
线程[28]--没抢到，票抢完了
线程[1]--获得了锁
线程[1]--没抢到，票抢完了
线程[14]--获得了锁
线程[14]--没抢到，票抢完了
线程[26]--获得了锁
线程[26]--没抢到，票抢完了
线程[34]--获得了锁
线程[34]--没抢到，票抢完了
线程[64]--获得了锁
线程[64]--没抢到，票抢完了
线程[96]--获得了锁
线程[96]--没抢到，票抢完了
线程[4]--获得了锁
线程[4]--没抢到，票抢完了
线程[55]--获得了锁
线程[55]--没抢到，票抢完了
线程[71]--获得了锁
线程[71]--没抢到，票抢完了
线程[81]--获得了锁
线程[81]--没抢到，票抢完了
线程[89]--获得了锁
线程[89]--没抢到，票抢完了
线程[21]--获得了锁
线程[21]--没抢到，票抢完了
线程[35]--获得了锁
线程[35]--没抢到，票抢完了
线程[54]--获得了锁
线程[54]--没抢到，票抢完了
线程[92]--获得了锁
线程[92]--没抢到，票抢完了
线程[60]--获得了锁
线程[60]--没抢到，票抢完了
线程[16]--获得了锁
线程[16]--没抢到，票抢完了
线程[32]--获得了锁
线程[32]--没抢到，票抢完了
线程[67]--获得了锁
线程[67]--没抢到，票抢完了
线程[25]--获得了锁
线程[25]--没抢到，票抢完了
线程[97]--获得了锁
线程[97]--没抢到，票抢完了
线程[98]--获得了锁
线程[98]--没抢到，票抢完了
线程[49]--获得了锁
线程[49]--没抢到，票抢完了
线程[56]--获得了锁
线程[56]--没抢到，票抢完了
线程[73]--获得了锁
线程[73]--没抢到，票抢完了
线程[65]--获得了锁
线程[65]--没抢到，票抢完了
线程[78]--获得了锁
线程[78]--没抢到，票抢完了
线程[85]--获得了锁
线程[85]--没抢到，票抢完了
线程[8]--获得了锁
线程[8]--没抢到，票抢完了
线程[72]--获得了锁
线程[72]--没抢到，票抢完了
线程[95]--获得了锁
线程[95]--没抢到，票抢完了
线程[84]--获得了锁
线程[84]--没抢到，票抢完了
线程[86]--获得了锁
线程[86]--没抢到，票抢完了
线程[46]--获得了锁
线程[46]--没抢到，票抢完了
线程[50]--获得了锁
线程[50]--没抢到，票抢完了
线程[23]--获得了锁
线程[23]--没抢到，票抢完了
线程[58]--获得了锁
线程[58]--没抢到，票抢完了
线程[9]--获得了锁
线程[9]--没抢到，票抢完了
线程[87]--获得了锁
线程[87]--没抢到，票抢完了
线程[36]--获得了锁
线程[36]--没抢到，票抢完了
线程[5]--获得了锁
线程[5]--没抢到，票抢完了
线程[62]--获得了锁
线程[62]--没抢到，票抢完了
线程[82]--获得了锁
线程[82]--没抢到，票抢完了
线程[91]--获得了锁
线程[91]--没抢到，票抢完了
线程[38]--获得了锁
线程[38]--没抢到，票抢完了
线程[44]--获得了锁
线程[44]--没抢到，票抢完了
线程[57]--获得了锁
线程[57]--没抢到，票抢完了
线程[51]--获得了锁
线程[51]--没抢到，票抢完了
线程[45]--获得了锁
线程[45]--没抢到，票抢完了
线程[41]--获得了锁
线程[41]--没抢到，票抢完了
线程[39]--获得了锁
线程[39]--没抢到，票抢完了
线程[75]--获得了锁
线程[75]--没抢到，票抢完了
线程[33]--获得了锁
线程[33]--没抢到，票抢完了
线程[61]--获得了锁
线程[61]--没抢到，票抢完了
线程[74]--获得了锁
线程[74]--没抢到，票抢完了
线程[10]--获得了锁
线程[10]--没抢到，票抢完了
线程[30]--获得了锁
线程[30]--没抢到，票抢完了
线程[59]--获得了锁
线程[59]--没抢到，票抢完了
线程[37]--获得了锁
线程[37]--没抢到，票抢完了
线程[40]--获得了锁
线程[40]--没抢到，票抢完了
线程[80]--获得了锁
线程[80]--没抢到，票抢完了
线程[19]--获得了锁
线程[19]--没抢到，票抢完了
线程[53]--获得了锁
线程[53]--没抢到，票抢完了
线程[11]--获得了锁
线程[11]--没抢到，票抢完了
线程[17]--获得了锁
线程[17]--没抢到，票抢完了
线程[66]--获得了锁
线程[66]--没抢到，票抢完了
线程[83]--获得了锁
线程[83]--没抢到，票抢完了
线程[15]--获得了锁
线程[15]--没抢到，票抢完了
线程[99]--获得了锁
线程[99]--没抢到，票抢完了
线程[18]--获得了锁
线程[18]--没抢到，票抢完了
线程[88]--获得了锁
线程[88]--没抢到，票抢完了
线程[79]--获得了锁
线程[79]--没抢到，票抢完了
线程[31]--获得了锁
线程[31]--没抢到，票抢完了
线程[42]--获得了锁
线程[42]--没抢到，票抢完了
线程[63]--获得了锁
线程[63]--没抢到，票抢完了
线程[47]--获得了锁
线程[47]--没抢到，票抢完了
线程[2]--获得了锁
线程[2]--没抢到，票抢完了
线程[24]--获得了锁
线程[24]--没抢到，票抢完了
线程[29]--获得了锁
线程[29]--没抢到，票抢完了
线程[3]--获得了锁
线程[3]--没抢到，票抢完了
线程[93]--获得了锁
线程[93]--没抢到，票抢完了
线程[69]--获得了锁
线程[69]--没抢到，票抢完了
线程[43]--获得了锁
线程[43]--没抢到，票抢完了
线程[0]--获得了锁
线程[0]--没抢到，票抢完了
线程[20]--获得了锁
线程[20]--没抢到，票抢完了
```
