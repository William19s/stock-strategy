import os
import pickle
from pathlib import Path
from typing import Any, Optional
from datetime import datetime, timedelta
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class Cache:
    """缓存管理"""
    
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get(self, key: str, ttl: Optional[int] = None) -> Any:
        """获取缓存"""
        try:
            cache_file = self.cache_dir / f"{key}.pkl"
            
            if not cache_file.exists():
                return None
            
            # 检查过期时间
            if ttl is not None:
                modified_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
                if datetime.now() - modified_time > timedelta(seconds=ttl):
                    return None
            
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
                
        except Exception as e:
            logger.error(f"读取缓存失败: {str(e)}")
            return None
    
    def set(self, key: str, value: Any) -> bool:
        """设置缓存"""
        try:
            cache_file = self.cache_dir / f"{key}.pkl"
            with open(cache_file, 'wb') as f:
                pickle.dump(value, f)
            return True
            
        except Exception as e:
            logger.error(f"写入缓存失败: {str(e)}")
            return False
    
    def clear(self, key: Optional[str] = None):
        """清除缓存"""
        try:
            if key is None:
                # 清除所有缓存
                for file in self.cache_dir.glob("*.pkl"):
                    file.unlink()
            else:
                # 清除指定缓存
                cache_file = self.cache_dir / f"{key}.pkl"
                if cache_file.exists():
                    cache_file.unlink()
                    
        except Exception as e:
            logger.error(f"清除缓存失败: {str(e)}") 