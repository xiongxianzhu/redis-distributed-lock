import time
import uuid
from threading import Thread

import redis
from redis import StrictRedis


class RedisLock(object):
    """
    基于Redis实现分布式锁
    """

    def __init__(self, redis_conn, prefix='lock', sleeptime=1):
        self.redis_conn = redis_conn
        self.prefix = prefix
        self.identifier = str(uuid.uuid4())
        self.sleeptime = sleeptime / 1000
        self.unlock_script = """
        if redis.call('get', KEYS[1]) == ARGV[1] then
            return redis.call('del', KEYS[1])
        else
            return 0
        end
        """

    def acquire(self, lock_name, expire=5000, acquire_timeout: int = None):
        """
        从redis连接获取一个redis分布式锁， 使用block模式

        :param lock_name: 锁的名称
        :param expire: redis key的过期时间 (millisecond)
        :param acquire_timeout: 锁的超时时间(second)
        :return:
        """
        if acquire_timeout:
            assert isinstance(acquire_timeout, int)
        lock_key = f'{self.prefix}:{lock_name}'
        while True:
            # 如果不存在这个锁则加锁并设置过期时间，避免死锁
            if self.redis_conn.set(
                    lock_key,
                    self.identifier,
                    nx=True,
                    px=expire):
                return True
            if acquire_timeout:
                if acquire_timeout <= 0:
                    return False
                acquire_timeout -= self.sleeptime
            time.sleep(self.sleeptime)

    def acquire_no_block(self, lock_name, expire=5000):
        """
        从redis连接获取一个redis分布式锁， 使用No-block模式

        :param lock_name: 锁的名称
        :param expire: redis key的过期时间 (millisecond)
        :return:
        """
        lock_key = f'{self.prefix}:{lock_name}'
        if self.redis_conn.set(lock_key, self.identifier, nx=True, px=expire):
            return True
        else:
            return False

    def release(self, lock_name):
        """
        释放锁

        :param lock_name: 锁的名称
        :return:
        """
        lock_key = f'{self.prefix}:{lock_name}'
        unlock_script = self.redis_conn.register_script(self.unlock_script)
        return unlock_script(keys=[lock_key], args=[self.identifier])


pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
redis_client = StrictRedis(connection_pool=pool)

count = 10


def sec_kill(i):
    lock = RedisLock(redis_client)
    lock_key = 'test'
    try:
        if lock.acquire(lock_key, expire=5000, acquire_timeout=2):
            print("线程[{}]--获得了锁".format(i))
            global count
            if count < 1:
                print("线程[{}]--没抢到，票抢完了".format(i))
                return
            count -= 1
            print("线程[{}]--抢到一张票，还剩{}张票".format(i, count))
    finally:
        lock.release(lock_key)
    print("线程[{}]--获得了锁".format(i))


if __name__ == '__main__':
    # 100个线程模拟秒杀10张票
    for i in range(100):
        t = Thread(target=sec_kill, args=(i,))
        t.start()
