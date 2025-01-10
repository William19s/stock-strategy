import baostock as bs
import pandas as pd
from typing import Optional, Dict
import logging
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class DataLoader:
    """数据加载类"""
    
    def __init__(self):
        self.cache: Dict[str, pd.DataFrame] = {}
    
    def get_stock_data(self, symbol: str, start_date: str = '2020-01-01') -> Optional[pd.DataFrame]:
        """获取股票数据"""
        try:
            # 检查缓存
            cache_key = f"{symbol}_{start_date}"
            if cache_key in self.cache:
                logger.info(f"Using cached data for {symbol}")
                return self.cache[cache_key]
            
            # 登录系统
            lg = bs.login()
            if lg.error_code != '0':
                logger.error(f"Login failed: {lg.error_msg}")
                return None
            
            # 获取数据
            rs = bs.query_history_k_data_plus(
                symbol,
                "date,open,high,low,close,volume,amount",
                start_date=start_date,
                frequency="d",
                adjustflag="3"
            )
            
            if rs.error_code != '0':
                logger.error(f"Query failed: {rs.error_msg}")
                return None
            
            # 处理数据
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            
            if not data_list:
                logger.warning(f"No data retrieved for {symbol}")
                return None
            
            # 创建DataFrame
            df = pd.DataFrame(data_list, columns=[
                'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Amount'
            ])
            
            # 数据类型转换
            numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Amount']
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
            df.set_index('Date', inplace=True)
            
            # 保存到缓存
            self.cache[cache_key] = df
            return df
            
        except Exception as e:
            logger.error(f"Error getting data for {symbol}: {str(e)}")
            return None
            
        finally:
            bs.logout()
    
    def get_stock_basic_info(self, symbol: str) -> Optional[Dict]:
        """获取股票基本信息"""
        try:
            lg = bs.login()
            rs = bs.query_stock_basic(code=symbol)
            
            if rs.error_code != '0':
                logger.error(f"Query failed: {rs.error_msg}")
                return None
            
            if rs.next():
                stock_info = rs.get_row_data()
                return {
                    'name': stock_info[1],
                    'market_cap': float(stock_info[11]) if stock_info[11] else 0,
                    'industry': stock_info[16],
                    'pe_ratio': float(stock_info[15]) if stock_info[15] else 0,
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting basic info for {symbol}: {str(e)}")
            return None
            
        finally:
            bs.logout() 