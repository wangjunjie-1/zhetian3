"""
数据库访问对象基类模块

该模块提供了数据库操作的基础功能，包括：
- 数据库连接管理
- 事务管理
- 错误处理
- 通用CRUD操作
"""
import logging
from typing import Any, List, Optional, Dict, Tuple
from contextlib import contextmanager
from dao.connectionPool import db_pool

class BaseDAO:
    """
    数据库访问对象基类
    
    提供基础的数据库操作功能，包括：
    - 数据库连接管理
    - 事务管理
    - 错误处理
    - 通用CRUD操作
    """
    
    def __init__(self):
        """初始化数据库访问对象"""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @contextmanager
    def get_cursor(self):
        """获取数据库游标"""
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                if cursor.rowcount > 0:  # 只有在有实际更改时才提交
                    conn.commit()
                else:
                    self.logger.debug("没有数据被修改，无需提交")
            except Exception as e:
                conn.rollback()
                self.logger.error(f"数据库操作错误: {str(e)}")
                raise
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """
        执行查询操作
        
        Args:
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            List[Tuple]: 查询结果列表
        """
        try:
            with self.get_cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"查询执行错误: {str(e)}")
            return []
    
    def execute_update(self, query: str, params: Optional[Tuple] = None) -> bool:
        """
        执行更新操作
        
        Args:
            query: SQL更新语句
            params: 更新参数
            
        Returns:
            bool: 操作是否成功
        """
        try:
            with self.get_cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return True
        except Exception as e:
            self.logger.error(f"更新执行错误: {str(e)}")
            return False
    
    def execute_many(self, query: str, params_list: List[tuple]) -> bool:
        """
        执行批量操作
        
        Args:
            query: SQL语句
            params_list: 参数列表
            
        Returns:
            bool: 操作是否成功
        """
        try:
            with self.get_cursor() as cursor:
                cursor.executemany(query, params_list)
                return True
        except Exception as e:
            self.logger.error(f"批量操作执行错误: {str(e)}")
            return False

    def close(self):
        """关闭数据库连接"""
        db_pool.close() 