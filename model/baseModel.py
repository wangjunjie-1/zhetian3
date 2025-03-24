"""
    所有用户类的基础类
    提供序列化和反序列化的抽象接口
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from core.eventmanager import EventManager

class BaseModel(ABC):
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """将对象转换为字典格式"""
        pass

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> None:
        """从字典格式加载数据到对象"""
        pass
