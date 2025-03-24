"""
玩家控制器模块

处理玩家相关的请求，协调服务层和视图层。
"""
import logging
from typing import Dict, Any, List
from service.playerService import PlayerService
from core.eventmanager import EventManager
from model.playerModel import PlayerModel
from utils.spiritroot import SpiritRoot

class PlayerController:
    """
    玩家控制器类
    
    处理玩家相关的请求，包括：
    - 创建玩家
    - 删除玩家
    - 获取玩家列表
    - 获取掌门详情
    - 更新玩家信息
    """
    
    def __init__(self, event_manager: EventManager):
        """
        初始化玩家控制器
        
        Args:
            event_manager: 事件管理器实例
        """
        self.service = PlayerService(event_manager)
        self.logger = logging.getLogger(self.__class__.__name__)
        if event_manager:
            self.event_manager=event_manager
    
    def init_master(self)->PlayerModel:
        """"
        游戏启动时，选择主角,不操作数据库
        """
        init_value = 100
        master = PlayerModel(self.event_manager)
        master.root = SpiritRoot(init_value).root_text
        master.isMaster = True
        return master

    def create_player(self, player:PlayerModel):
        """
        创建新玩家
        
        Args:
            player_data: 玩家数据字典
            
        Returns:
            Dict[str, Any]: 响应结果
        """
        try:
            ret  = self.service.create_player(player)
            if ret:
                return {
                    'success': True,
                    'message': '创建玩家成功',
                    'data': ret.to_dict()
                }
            return {
                'success': False,
                'message': '创建玩家失败',
                'data': None
            }
        except Exception as e:
            self.logger.error(f"创建玩家异常: {str(e)}")
            return {
                'success': False,
                'message': f'系统错误: {str(e)}',
                'data': None
            }
    
    def delete_player(self, player_id: int) -> Dict[str, Any]:
        """
        删除玩家
        
        Args:
            player_id: 玩家ID
            
        Returns:
            Dict[str, Any]: 响应结果
        """
        try:
            success = self.service.delete_player(player_id)
            if success:
                return {
                    'success': True,
                    'message': '删除玩家成功',
                    'data': None
                }
            return {
                'success': False,
                'message': '删除玩家失败',
                'data': None
            }
        except Exception as e:
            self.logger.error(f"删除玩家异常: {str(e)}")
            return {
                'success': False,
                'message': f'系统错误: {str(e)}',
                'data': None
            }
    
    def get_player_list(self) -> Dict[str, Any]:
        """
        获取玩家列表
        
        Returns:
            Dict[str, Any]: 响应结果
        """
        try:
            players = self.service.get_all_players()
            return {
                'success': True,
                'message': '获取玩家列表成功',
                'data': [p.to_dict() for p in players]
            }
        except Exception as e:
            self.logger.error(f"获取玩家列表异常: {str(e)}")
            return {
                'success': False,
                'message': f'系统错误: {str(e)}',
                'data': None
            }
    
    def get_master_details(self) -> Dict[str, Any]:
        """
        获取掌门详情
        
        Returns:
            Dict[str, Any]: 响应结果
        """
        try:
            master_details = self.service.get_master_details()
            return {
                'success': True,
                'message': '获取掌门详情成功',
                'data': master_details
            }
        except Exception as e:
            self.logger.error(f"获取掌门详情异常: {str(e)}")
            return {
                'success': False,
                'message': f'系统错误: {str(e)}',
                'data': None
            }
    
    def update_player(self, player_id: int, player_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新玩家信息
        
        Args:
            player_id: 玩家ID
            player_data: 更新的玩家数据
            
        Returns:
            Dict[str, Any]: 响应结果
        """
        try:
            player = self.service.update_player(player_id, player_data)
            if player:
                return {
                    'success': True,
                    'message': '更新玩家成功',
                    'data': player.to_dict()
                }
            return {
                'success': False,
                'message': '更新玩家失败',
                'data': None
            }
        except Exception as e:
            self.logger.error(f"更新玩家异常: {str(e)}")
            return {
                'success': False,
                'message': f'系统错误: {str(e)}',
                'data': None
            }
    
    def get_player_with_companion(self, player_id: int) -> Dict[str, Any]:
        """
        获取玩家及其伴侣信息
        
        Args:
            player_id: 玩家ID
            
        Returns:
            Dict[str, Any]: 响应结果
        """
        try:
            result = self.service.get_player_with_companion(player_id)
            if result:
                return {
                    'success': True,
                    'message': '获取玩家及伴侣信息成功',
                    'data': result
                }
            return {
                'success': False,
                'message': '未找到玩家信息',
                'data': None
            }
        except Exception as e:
            self.logger.error(f"获取玩家及伴侣信息异常: {str(e)}")
            return {
                'success': False,
                'message': f'系统错误: {str(e)}',
                'data': None
            }

