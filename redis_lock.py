import time
import uuid

__all__ = [
    'RedisLock'
]


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
        :param acquire_timeout: 锁的超时时间
        :return:
        """
        if timeout:
            assert isinstance(timeout, int)
        lockname = f'{self.prefix}:{self.lock_name}'
        while True:
            # 如果不存在这个锁则加锁并设置过期时间，避免死锁
            if self.redis_conn.set(lockname, self.identifier, nx=True, px=expire):
                return True
            if acquire_timeout:
                if acquire_timeout <= 0:
                    return False
                acquire_timeout -= self.sleeptime
            time.sleep(self.sleeptime)

    def acquire_no_block(self, lock_name, expire=5000):
        """
        从redis连接获取一个redis分布式锁， 使用No-block模式
        """
        lockname = f'{self.prefix}:{self.lock_name}'
        if self.redis_conn.set(lockname, self.identifier, nx=True, px=expire):
            return True
        else:
            return False

    def release(self, lock_name):
        """
        释放锁

        :param lock_name: 锁的名称
        :return:
        """
        lockname = f'{self.prefix}:{self.lock_name}'
        unlock_script = self.redisconn.register_script(self.unlock_script)
        return unlock_script(keys=[lockname], args=[self.identifier])
