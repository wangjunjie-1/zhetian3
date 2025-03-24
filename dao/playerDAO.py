"""
玩家数据访问对象模块

该模块提供了与数据库交互的接口，用于玩家数据的持久化存储和读取。
使用 SQLite 数据库实现。
"""
import logging
from typing import Optional, List
from dao.baseDAO import BaseDAO
from model.playerModel import PlayerModel

class PlayerDAO(BaseDAO):
    """
    玩家数据访问对象
    
    负责处理玩家数据的数据库操作，包括：
    - 创建玩家数据表
    - 插入新玩家数据
    - 更新玩家数据
    - 查询玩家数据
    - 软删除玩家数据（将is_dead设置为True）
    """
    
    def __init__(self):
        """初始化玩家DAO"""
        super().__init__()  # 不再传入 db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """初始化数据库表结构"""
        self.execute_update('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER DEFAULT 0,
                sex INTEGER DEFAULT 0,
                is_master INTEGER DEFAULT 0,
                is_dead INTEGER DEFAULT 0,
                father_id INTEGER DEFAULT -1,
                mother_id INTEGER DEFAULT -1,
                teacher_id INTEGER DEFAULT -1,
                companion_id INTEGER DEFAULT -1,
                root TEXT,
                attribute TEXT,
                base_breakup_probability REAL DEFAULT -1,
                realm_level INTEGER DEFAULT 1,
                current_exp REAL DEFAULT 0.0
            )
        ''')
        self.logger.debug("数据库表初始化完成")
    
    def insert(self, player: PlayerModel) -> bool:
        """插入新玩家数据"""
        query = '''
            INSERT INTO players (
                name, age, sex, is_master, is_dead,
                father_id, mother_id, teacher_id, companion_id,
                root, attribute, base_breakup_probability,
                realm_level, current_exp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            player.name, player.age, player.sex,
            player.isMaster, player.isDead,
            player.father_id, player.mother_id, player.teacher_id,
            player.companion_id, player.root, player.attribute,
            player.base_breakup_probability,
            player.realm_level, player.current_exp
        )
        
        success = self.execute_update(query, params)
        if success:
            self.logger.debug(f"成功插入玩家数据: {player.name}")
        return success
    
    def update(self, player: PlayerModel) -> bool:
        """更新玩家数据"""
        query = '''
            UPDATE players SET
                name = ?, age = ?, sex = ?,
                is_master = ?, is_dead = ?,
                father_id = ?, mother_id = ?,
                teacher_id = ?, companion_id = ?,
                root = ?, attribute = ?,
                base_breakup_probability = ?,
                realm_level = ?, current_exp = ?
            WHERE id = ?
        '''
        params = (
            player.name, player.age, player.sex,
            player.isMaster, player.isDead,
            player.father_id, player.mother_id,
            player.teacher_id, player.companion_id,
            player.root, player.attribute,
            player.base_breakup_probability,
            player.realm_level, player.current_exp,
            player.id
        )
        
        success = self.execute_update(query, params)
        if success:
            self.logger.debug(f"成功更新玩家数据: {player.name} (ID={player.id})")
        else:
            self.logger.warning(f"更新玩家数据失败: {player.name} (ID={player.id})")
            # 可以在这里添加更多的诊断信息
            self.logger.debug(f"更新参数: {params}")
        return success
    
    def get_by_id(self, player_id: int) -> Optional[PlayerModel]:
        """
        根据ID查询玩家数据（不包括已删除的玩家）
        
        Args:
            player_id: 玩家ID
            
        Returns:
            Optional[PlayerModel]: 玩家对象，如果不存在则返回None
        """
        query = 'SELECT * FROM players WHERE id = ? AND is_dead = 0'
        rows = self.execute_query(query, (player_id,))
        
        if rows:
            row = rows[0]
            player = self._row_to_player(row)
            
            self.logger.debug(f"成功查询玩家数据: {player.name}")
            return player
        return None
    
    def get_all(self) -> List[PlayerModel]:
        """
        获取所有未删除的玩家数据
        
        Returns:
            List[PlayerModel]: 玩家对象列表
        """
        query = 'SELECT * FROM players WHERE is_dead = 0'
        rows = self.execute_query(query)
        
        players = []
        for row in rows:
            player = self._row_to_player(row)
            players.append(player)
        
        self.logger.debug(f"成功查询所有未删除的玩家数据，共 {len(players)} 条")
        return players
    
    def fake_delete(self, player_id: int) -> bool:
        """
        软删除玩家数据（将is_dead设置为True）
        
        Args:
            player_id: 要删除的玩家ID
            
        Returns:
            bool: 删除是否成功
        """
        query = '''
            UPDATE players 
            SET is_dead = 1 
            WHERE id = ? AND is_dead = 0
        '''
        success = self.execute_update(query, (player_id,))
        if success:
            self.logger.debug(f"成功软删除玩家数据: ID={player_id}")
        return success

    def get_by_parent_id(self, parent_id: int, is_father: bool = True) -> List[PlayerModel]:
        """
        根据父母ID查询玩家数据
        
        Args:
            parent_id: 父母的ID
            is_father: True表示查询父亲ID，False表示查询母亲ID
            
        Returns:
            List[PlayerModel]: 符合条件的玩家列表
        """
        query = '''
            SELECT * FROM players 
            WHERE is_dead = 0 
            AND {} = ?
        '''.format('father_id' if is_father else 'mother_id')
        
        rows = self.execute_query(query, (parent_id,))
        players = []
        
        for row in rows:
            player = self._row_to_player(row)
            players.append(player)
        
        relation = "父亲" if is_father else "母亲"
        self.logger.debug(f"成功查询{relation} ID={parent_id} 的所有子女，共 {len(players)} 人")
        return players

    def get_by_teacher_id(self, teacher_id: int) -> List[PlayerModel]:
        """
        根据师父ID查询玩家数据（徒弟列表）
        
        Args:
            teacher_id: 师父的ID
            
        Returns:
            List[PlayerModel]: 符合条件的玩家列表
        """
        query = '''
            SELECT * FROM players 
            WHERE is_dead = 0 
            AND teacher_id = ?
        '''
        
        rows = self.execute_query(query, (teacher_id,))
        players = []
        
        for row in rows:
            player = self._row_to_player(row)
            players.append(player)
        
        self.logger.debug(f"成功查询师父 ID={teacher_id} 的所有徒弟，共 {len(players)} 人")
        return players

    def get_all_masters(self) -> List[PlayerModel]:
        """
        查询所有掌门
        
        Returns:
            List[PlayerModel]: 掌门列表
        """
        query = '''
            SELECT * FROM players 
            WHERE is_dead = 0 
            AND is_master = 1
        '''
        
        rows = self.execute_query(query)
        players = []
        
        for row in rows:
            player = self._row_to_player(row)
            players.append(player)
        
        self.logger.debug(f"成功查询所有掌门，共 {len(players)} 人")
        return players

    def _row_to_player(self, row: tuple) -> PlayerModel:
        """将数据库行转换为玩家对象"""
        player = PlayerModel(None)  # 临时创建，实际使用时需要传入event_manager
        player.id = row[0]
        player.name = row[1]
        player.age = row[2]
        player.sex = row[3]
        player.isMaster = row[4]
        player.isDead = row[5]
        player.father_id = row[6]
        player.mother_id = row[7]
        player.teacher_id = row[8]
        player.companion_id = row[9]
        player.root = row[10]
        player.attribute = row[11]
        player.base_breakup_probability = row[12]
        player.realm_level = row[13]
        player.current_exp = row[14]
        return player 