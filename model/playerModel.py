"""
玩家模型模块

该模块定义了游戏中的玩家类，继承自BaseModel。
负责管理玩家的基本属性、状态和相关操作。

主要功能：
- 玩家基础属性管理
- 玩家存档加载与保存
- 玩家修炼系统对接
"""
import logging
from typing import Dict, Any
from model.baseModel import BaseModel
from core.eventmanager import EventManager

REALMS = [
    {"name": "凡人境","probability":0.99,"exp_required": 0,           "spirit_power": 0, "spirit_sense": 0,             "lifespan": 100},
    {"name": "炼气境","probability":0.9,"exp_required": 100,          "spirit_power": 10, "spirit_sense": 5,            "lifespan": 150},
    {"name": "筑基境","probability":0.8,"exp_required": 1000,         "spirit_power": 50, "spirit_sense": 20,           "lifespan": 300},
    {"name": "金丹境","probability":0.7,"exp_required": 10000,        "spirit_power": 200, "spirit_sense": 100,         "lifespan": 500},
    {"name": "元婴境","probability":0.6,"exp_required": 100000,       "spirit_power": 1000, "spirit_sense": 500,        "lifespan": 1000},
    {"name": "化神境","probability":0.5,"exp_required": 1000000,      "spirit_power": 5000, "spirit_sense": 2000,       "lifespan": 2000},
    {"name": "合体境","probability":0.4,"exp_required": 10000000,     "spirit_power": 20000, "spirit_sense": 10000,     "lifespan": 5000},
    {"name": "大乘境","probability":0.3,"exp_required": 100000000,    "spirit_power": 100000, "spirit_sense": 50000,    "lifespan": 10000},
    {"name": "渡劫境","probability":0.2,"exp_required": 1000000000,   "spirit_power": 500000, "spirit_sense": 200000,   "lifespan": 20000},
    {"name": "真仙境","probability":0.0,"exp_required": 10000000000,  "spirit_power": 2000000, "spirit_sense": 1000000, "lifespan": -1},  # 长生不老
]


class PlayerModel(BaseModel):
    """
    玩家类
    
    管理玩家的基本属性和行为，包括：
    - 基础个人信息（ID、姓名、年龄等）
    - 家族关系（父母、师承等）
    - 伴侣关系
    - 修炼相关属性
    
    Attributes:
        id (int): 玩家唯一标识
        name (str): 玩家名称
        age (int): 玩家年龄
        sex (int): 性别，0为女，1为男
        isMaster (int): 是否为掌门，0否1是
        isDead (int): 是否死亡，0否1是
        father_id (int): 父亲ID
        mother_id (int): 母亲ID
        teacher_id (int): 师父ID
        companion_id (int): 伴侣ID
        root (str): 灵根类型
        attribute (str): 玩家属性
        base_breakup_probability (float): 基础突破概率
        realm_level (int): 境界等级
        current_exp (int): 当前经验值
    """
    
    def __init__(self, event_manager: EventManager):
        """
        初始化玩家实例
        
        Args:
            event_manager: 事件管理器实例
        """
        super().__init__(event_manager)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # 基础属性初始化
        self.id: int = -1
        self.name: str = '龙傲天'
        self.age: int = 0
        self.sex: int = 0
        self.isMaster: int = 0
        self.isDead: int = 0
        self.father_id: int = -1
        self.mother_id: int = -1
        self.teacher_id: int = -1
        self.companion_id: int = -1
        self.root: str = ""
        self.attribute: str = ""
        self.base_breakup_probability: float = -1
        self.realm_level: int = 1
        self.current_exp: int = 0

        # 注册时间流逝事件
        if event_manager:
            self.event_manager = event_manager
            self.event_manager.subscribe('time_pass', self.cultivate)
        
    def to_dict(self) -> Dict[str, Any]:
        """
        将玩家数据序列化为字典格式
        
        Returns:
            Dict[str, Any]: 包含玩家所有属性的字典
        """
        data = {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'sex': self.sex,
            'isMaster': self.isMaster,
            'isDead': self.isDead,
            'father_id': self.father_id,
            'mother_id': self.mother_id,
            'teacher_id': self.teacher_id,
            'companion_id': self.companion_id,
            'root': self.root,
            'attribute': self.attribute,
            'base_breakup_probability': self.base_breakup_probability,
            'realm_level': self.realm_level,
            'current_exp': self.current_exp
        }
        self.logger.debug(f"序列化玩家数据: {self.name}")
        return data

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        从字典格式反序列化数据到玩家对象
        
        Args:
            data: 包含玩家属性的字典
        """
        self.id = data.get('id', self.id)
        self.name = data.get('name', self.name)
        self.age = data.get('age', self.age)
        self.sex = data.get('sex', self.sex)
        self.isMaster = data.get('isMaster', self.isMaster)
        self.isDead = data.get('isDead', self.isDead)
        self.father_id = data.get('father_id', self.father_id)
        self.mother_id = data.get('mother_id', self.mother_id)
        self.teacher_id = data.get('teacher_id', self.teacher_id)
        self.companion_id = data.get('companion_id', self.companion_id)
        self.root = data.get('root', self.root)
        self.attribute = data.get('attribute', self.attribute)
        self.base_breakup_probability = data.get('base_breakup_probability', self.base_breakup_probability)
        self.realm_level = data.get('realm_level', self.realm_level)
        self.current_exp = data.get('current_exp', self.current_exp)
        
        self.logger.debug(f"反序列化玩家数据: {self.name}")

    @property
    def get_realm_cur(self)->dict:
        return REALMS[self.realm_level]
    
    @property  
    def get_realm_next(self):
        if self.realm_level ==  len(REALMS):
            return self.get_realm_cur
        else:
            return REALMS[self.realm_level+1]

    def cultivate(self, *args, **kwargs) -> None:
        """
        修炼方法，响应时间流逝事件
        
        在每个时间单位进行修炼相关计算
        """
        # TODO: 实现具体的修炼逻辑
        self.logger.debug(f"玩家 {self.name} 正在修炼")