"""
玩家服务层模块

处理玩家相关的业务逻辑，连接控制层和数据访问层。
"""
import logging
from typing import List, Optional, Dict, Any
from dao.playerDAO import PlayerDAO
from model.playerModel import PlayerModel
from core.eventmanager import EventManager

class PlayerService:
    """
    玩家服务类
    
    处理玩家相关的业务逻辑，包括：
    - 创建和初始化玩家
    - 玩家数据的增删改查
    - 特殊玩家（如掌门）的处理
    """
    
    def __init__(self, event_manager: EventManager):
        """
        初始化玩家服务
        
        Args:
            event_manager: 事件管理器实例
        """
        self.event_manager = event_manager
        self.player_dao = PlayerDAO()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def create_player(self, player:PlayerModel) -> Optional[PlayerModel]:
        """
        创建新玩家
        
        Args:
            player_data: 包含玩家信息的字典
            
        Returns:
            Optional[PlayerModel]: 创建的玩家对象，失败则返回None
        """
        try:            
            # 保存到数据库
            if self.player_dao.insert(player):
                self.logger.info(f"成功创建玩家: {player.name}")
                return player
            return None
        except Exception as e:
            self.logger.error(f"创建玩家失败: {str(e)}")
            return None
    
    def delete_player(self, player_id: int) -> bool:
        """
        删除玩家（软删除）
        
        Args:
            player_id: 玩家ID
            
        Returns:
            bool: 删除是否成功
        """
        try:
            if self.player_dao.fake_delete(player_id):
                self.logger.info(f"成功删除玩家 ID={player_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"删除玩家失败: {str(e)}")
            return False
    
    def get_all_players(self) -> List[PlayerModel]:
        """
        获取所有玩家列表
        
        Returns:
            List[PlayerModel]: 玩家列表
        """
        try:
            players = self.player_dao.get_all()
            self.logger.info(f"成功获取所有玩家列表，共 {len(players)} 人")
            return players
        except Exception as e:
            self.logger.error(f"获取玩家列表失败: {str(e)}")
            return []
    
    def get_master(self) -> List[dict]:
        """
        获取所有掌门的详细信息
        
        Returns:
            List[dict]: 掌门详细信息列表，包括徒弟数量等
        """
        try:
            masters = self.player_dao.get_all_masters()
            master_details = []
            
            for master in masters:
                disciples = self.player_dao.get_all_masters(master.id)[0]
                detail = master.to_dict()
                detail['disciple_count'] = len(disciples)
                master_details.append(detail)
            
            self.logger.info(f"成功获取掌门详情，共 {len(masters)} 人")
            return master_details
        except Exception as e:
            self.logger.error(f"获取掌门详情失败: {str(e)}")
            return []
    
    def update_player(self, player_id: int, player_data: dict) -> Optional[PlayerModel]:
        """
        更新玩家信息
        
        Args:
            player_id: 玩家ID
            player_data: 更新的玩家数据
            
        Returns:
            Optional[PlayerModel]: 更新后的玩家对象，失败则返回None
        """
        try:
            # 先获取现有玩家数据
            player = self.player_dao.get_by_id(player_id)
            if not player:
                self.logger.error(f"未找到玩家 ID={player_id}")
                return None
            
            # 更新玩家数据
            player.from_dict(player_data)
            # 保存到数据库
            if self.player_dao.update(player):
                self.logger.info(f"成功更新玩家: {player.name}")
                return player
            return None
        except Exception as e:
            self.logger.error(f"更新玩家失败: {str(e)}")
            return None

    def get_player_with_companion(self, player_id: int) -> Optional[Dict[str, Any]]:
        """
        获取玩家及其伴侣信息
        
        Args:
            player_id: 玩家ID
            
        Returns:
            Optional[Dict[str, Any]]: 包含玩家和伴侣信息的字典
        """
        try:
            player = self.player_dao.get_by_id(player_id)
            if not player:
                return None
                
            result = player.to_dict()
            
            if player.companion_id > 0:
                companion = self.player_dao.get_by_id(player.companion_id)
                if companion:
                    result['companion'] = companion.to_dict()
                    
            return result
        except Exception as e:
            self.logger.error(f"获取玩家及伴侣信息失败: {str(e)}")
            return None
