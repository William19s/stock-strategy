import time
import functools
from typing import Callable
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

def performance_monitor(func: Callable):
    """性能监控装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        logger.info(f"{func.__name__} 执行时间: {duration:.3f}秒")
        if duration > 5:
            logger.warning(f"{func.__name__} 执行时间过长: {duration:.3f}秒")
        
        return result
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0):
    """重试装饰器"""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"{func.__name__} 重试{max_attempts}次后失败: {str(e)}")
                        raise
                    logger.warning(f"{func.__name__} 第{attempts}次重试")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator 