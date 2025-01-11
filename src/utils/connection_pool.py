import baostock as bs
from typing import Optional
import threading
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ConnectionPool:
    """BaoStock连接池"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance
    
    def __init__(self):
        self._pool = []
        self._max_size = 5
        self._lock = threading.Lock()
    
    def get_connection(self) -> Optional[bs]:
        """获取连接"""
        with self._lock:
            if not self._pool:
                try:
                    lg = bs.login()
                    if lg.error_code != '0':
                        logger.error(f"登录失败: {lg.error_msg}")
                        return None
                    return bs
                except Exception as e:
                    logger.error(f"创建连接失败: {str(e)}")
                    return None
            return self._pool.pop()
    
    def release_connection(self, conn):
        """释放连接"""
        with self._lock:
            if len(self._pool) < self._max_size:
                self._pool.append(conn)
            else:
                try:
                    bs.logout()
                except:
                    pass
    
    def close_all(self):
        """关闭所有连接"""
        with self._lock:
            for _ in range(len(self._pool)):
                conn = self._pool.pop()
                try:
                    bs.logout()
                except:
                    pass 