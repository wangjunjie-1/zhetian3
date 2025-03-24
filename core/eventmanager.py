"""
事件管理器模块
用于实现发布-订阅模式的事件系统，支持事件的订阅、发布和取消订阅。

主要功能：
- 支持多线程安全的事件订阅和发布
- 支持事件监听器的添加和移除
- 支持事件的异步触发和结果收集
"""
import logging
from threading import Lock
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

class EventManager:
    """
    事件管理器类
    
    负责管理事件的订阅关系和事件的触发分发。
    所有操作都是线程安全的。
    
    Attributes:
        _lock (Lock): 线程锁，用于保护事件监听器字典的并发访问
        _listeners (Dict[str, List[Callable]]): 存储事件类型到监听器列表的映射
    """
    
    def __init__(self):
        """初始化事件管理器"""
        self._lock = Lock()
        self._listeners: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, listener: Callable) -> bool:
        """
        订阅指定类型的事件
        
        Args:
            event_type: 事件类型标识符
            listener: 事件监听器函数
            
        Returns:
            bool: 订阅是否成功
            
        Raises:
            TypeError: 当listener不是可调用对象时抛出
        """
        if not callable(listener):
            raise TypeError("监听器必须是可调用对象")
            
        with self._lock:
            if event_type not in self._listeners:
                self._listeners[event_type] = []
            if listener not in self._listeners[event_type]:
                self._listeners[event_type].append(listener)
                logger.debug(f"成功订阅事件: {event_type}")
                return True
            logger.debug(f"监听器已存在，忽略重复订阅: {event_type}")
            return False

    def unsubscribe(self, event_type: str, listener: Callable) -> bool:
        """
        取消订阅指定类型的事件
        
        Args:
            event_type: 事件类型标识符
            listener: 要移除的事件监听器函数
            
        Returns:
            bool: 取消订阅是否成功
        """
        with self._lock:
            if event_type in self._listeners and listener in self._listeners[event_type]:
                self._listeners[event_type].remove(listener)
                logger.debug(f"成功取消订阅事件: {event_type}")
                # 如果该事件类型没有监听器了，清理该事件类型
                if not self._listeners[event_type]:
                    del self._listeners[event_type]
                return True
            logger.debug(f"未找到要取消的订阅: {event_type}")
            return False

    def publish(self, event_type: str, *args: Any, **kwargs: Any) -> List[Any]:
        """
        发布事件，触发所有相关的监听器
        
        Args:
            event_type: 事件类型标识符
            *args: 传递给监听器的位置参数
            **kwargs: 传递给监听器的关键字参数
            
        Returns:
            List[Any]: 所有监听器的返回值列表
            
        Note:
            - 监听器的执行在锁外进行，以避免长时间持有锁
            - 如果监听器执行出错，会记录错误但不影响其他监听器的执行
        """
        # 在锁保护下复制监听器列表，避免执行回调时持有锁
        with self._lock:
            listeners = self._listeners.get(event_type, [])[:]
        
        if not listeners:
            logger.debug(f"没有找到事件 {event_type} 的监听器")
            return []
            
        results = []
        for listener in listeners:
            try:
                result = listener(*args, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"执行事件监听器时出错: {event_type}, 错误: {str(e)}", exc_info=True)
                results.append(None)
                
        return results

    def clear(self, event_type: Optional[str] = None) -> None:
        """
        清除指定事件类型或所有事件类型的监听器
        
        Args:
            event_type: 要清除的事件类型，如果为None则清除所有事件
        """
        with self._lock:
            if event_type is None:
                self._listeners.clear()
                logger.debug("已清除所有事件监听器")
            elif event_type in self._listeners:
                del self._listeners[event_type]
                logger.debug(f"已清除事件类型 {event_type} 的所有监听器")
