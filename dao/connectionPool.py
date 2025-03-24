"""
数据库连接池模块

提供全局唯一的数据库连接池，统一管理所有数据库连接。
"""
import sqlite3
import logging
from typing import Optional
from contextlib import contextmanager
from threading import Lock

class DatabaseConnectionPool:
    """单例模式的数据库连接池"""
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.logger = logging.getLogger(self.__class__.__name__)
            self._conn: Optional[sqlite3.Connection] = None
            self._lock = Lock()
            self._initialized = True
            self._db_path = None
    
    def initialize(self, db_path: str):
        """
        初始化连接池
        
        Args:
            db_path: 数据库文件路径
        """
        with self._lock:
            self._db_path = db_path
            self.logger.info(f"初始化数据库连接池: {db_path}")
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接"""
        if not self._db_path:
            raise RuntimeError("数据库连接池未初始化，请先调用 initialize 方法")
            
        with self._lock:
            if self._conn is None:
                try:
                    self._conn = sqlite3.connect(self._db_path)
                    self.logger.debug("创建新的数据库连接")
                except sqlite3.Error as e:
                    self.logger.error(f"数据库连接错误: {str(e)}")
                    raise
            
        try:
            yield self._conn
        except Exception as e:
            self.logger.error(f"数据库操作错误: {str(e)}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        with self._lock:
            if self._conn:
                self._conn.close()
                self._conn = None
                self.logger.debug("关闭数据库连接")

# 全局连接池实例
db_pool = DatabaseConnectionPool() 