import time
import functools
from typing import Callable, Any
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

def timeit(func: Callable) -> Callable:
    """函数执行时间装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(f"{func.__name__} 执行时间: {end - start:.2f}秒")
        return result
    return wrapper

class Profiler:
    """性能分析器"""
    
    def __init__(self):
        self.records = {}
    
    def start(self, name: str):
        """开始计时"""
        self.records[name] = time.perf_counter()
    
    def end(self, name: str) -> float:
        """结束计时"""
        if name not in self.records:
            return 0
        
        duration = time.perf_counter() - self.records[name]
        logger.info(f"{name} 执行时间: {duration:.2f}秒")
        return duration
    
    def clear(self):
        """清除记录"""
        self.records.clear() 