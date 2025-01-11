import re
from typing import Optional
from .logger import setup_logger

logger = setup_logger(__name__)

def validate_stock_code(code: str) -> bool:
    """验证股票代码格式"""
    try:
        # 匹配 sh.600000 或 sz.000001 格式
        pattern = r'^(sh|sz)\.\d{6}$'
        return bool(re.match(pattern, code))
    except Exception as e:
        logger.error(f"股票代码验证失败: {str(e)}")
        return False

def validate_date_format(date_str: str) -> bool:
    """验证日期格式 YYYY-MM-DD"""
    try:
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return bool(re.match(pattern, date_str))
    except Exception as e:
        logger.error(f"日期格式验证失败: {str(e)}")
        return False 