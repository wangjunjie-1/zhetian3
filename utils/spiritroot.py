import random
import math
import logging
logger = logging.getLogger()
class SpiritRoot:
    # 定义灵根属性及其权重
    BASE_ATTRIBUTES = {
        '金': 0.2,
        '木': 0.2,
        '水': 0.2,
        '火': 0.2,
        '土': 0.2,
    }
    
    ADVANCED_ATTRIBUTES = {
        '风': 0.1,  # 高级属性权重更高
        '冰': 0.1,
        '空': 0.05,
    }
    
    # 定义灵根级别及其权重
    LEVELS = {
        '普通': 0.7,
        '变异': 0.2,
        '地': 0.08,
        '天': 0.02,
    }
    
    # 灵根数量的分布权重（灵根越多，几率越小）
    ATTRIBUTE_COUNT_WEIGHTS = [0.4, 0.3, 0.2, 0.08, 0.02]  # 1到5个灵根的权重
    
    def __init__(self,value=None):
        if value is None:
            # 生成灵根文本
            self.root_text = self._generate_root_text()
            self.value = self.calculate_value(self.root_text)
        else:
            while(True):
                self.root_text = self._generate_root_text()
                self.value = self.calculate_value(self.root_text)
                if abs(self.value-value)/value <0.1:
                    break


    @classmethod
    def _generate_root_text(cls):
        """生成灵根文本描述"""
        # 合并基础属性和高级属性
        all_attributes = {**cls.BASE_ATTRIBUTES, **cls.ADVANCED_ATTRIBUTES}
        
        # 随机选择灵根数量
        attribute_count = random.choices(
            range(1, 6),
            weights=cls.ATTRIBUTE_COUNT_WEIGHTS,
            k=1
        )[0]
        
        # 随机选择属性
        attributes = random.choices(
            list(all_attributes.keys()),
            weights=list(all_attributes.values()),
            k=attribute_count
        )
        
        # 随机选择级别
        level = random.choices(
            list(cls.LEVELS.keys()),
            weights=list(cls.LEVELS.values()),
            k=1
        )[0]

        unique_attributes = list(set(attributes))  # 去重
        attributes_str = ''.join(unique_attributes)  # 用逗号连接
        return f"{attributes_str}_{level}"
    
    @classmethod
    def display_text(cls,root_text):
        attributes,level = cls.split_root_text(root_text)
        """返回格式化的灵根显示文本"""
        name_map = {1: '单', 2: '双', 3: '三', 4: '四', 5: '五'}
        sorted_attributes = ''.join(
            [attr for attr in cls.BASE_ATTRIBUTES if attr in attributes] +
            [attr for attr in cls.ADVANCED_ATTRIBUTES if attr in attributes]
        )
        return f"{sorted_attributes} {level} {name_map[len(attributes)]}灵根"

    @classmethod
    def split_root_text(cls, root_text):
        """改进的分割方法，增加错误处理和类型检查"""
        if not isinstance(root_text, str):
            raise TypeError('Root text must be a string')
            
        if '-' in root_text:
            attributes_str, level = root_text.split('-')
        elif '_' in root_text:      
            attributes_str, level = root_text.split('_')
        else:
            raise ValueError('Invalid root text format: must contain "-" or "_"')
            
        # 将字符串转换为属性列表
        # attributes = eval(attributes_str) if isinstance(eval(attributes_str), list) else []
        
        return attributes_str, level

    @classmethod
    def check_legal(cls, root_text):
        """改进的合法性检查方法"""
        try:
            attributes, level = cls.split_root_text(root_text)
            
            # 检查属性是否合法
            valid_attributes = set(cls.BASE_ATTRIBUTES.keys()) | set(cls.ADVANCED_ATTRIBUTES.keys())
            if not all(attr in valid_attributes for attr in attributes):
                return False
                
            # 检查属性数量
            if not 1 <= len(attributes) <= 5:
                return False
                
            # 检查级别是否合法
            if level not in cls.LEVELS:
                return False
                
            return True
            
        except (ValueError, TypeError, SyntaxError):
            return False
    
    @classmethod
    def calculate_cultivation_coefficient(cls,root_text):
        attributes,level = SpiritRoot.split_root_text(root_text)
        # 基础修炼系数：每个基础属性为1，每个高级属性为2
        base_coefficient = 0
        for attr in attributes:
            if attr in SpiritRoot.BASE_ATTRIBUTES:
                base_coefficient += 1
            elif attr in SpiritRoot.ADVANCED_ATTRIBUTES:
                base_coefficient += 2
        
        # 多灵根加成系数（非线性增长，使用对数增长）
        attribute_count = len(attributes)
        if attribute_count == 1:
            multi_attr_bonus = 1.0  # 单灵根无加成
        else:
            multi_attr_bonus = 1.1**attribute_count  # 对数增长
        
        # 灵根级别加成
        level_bonus = {
            '普通': 1.0,
            '变异': 1.5,
            '地': 2.0,
            '天': 3.0,
        }.get(level, 1.0)
        
        # 总修炼系数
        total_coefficient = (base_coefficient * multi_attr_bonus) * level_bonus 
        return round(total_coefficient,2)
    

    @classmethod
    def calculate_probability(cls, attributes, level):
        """计算特定灵根组合出现的概率"""
        # 计算属性组合的概率
        all_attributes = {**cls.BASE_ATTRIBUTES, **cls.ADVANCED_ATTRIBUTES}
        attr_prob = 1.0
        for attr in attributes:
            attr_prob *= all_attributes[attr]
            
        # 计算数量的概率
        count_prob = cls.ATTRIBUTE_COUNT_WEIGHTS[len(attributes) - 1]
        
        # 计算级别的概率
        level_prob = cls.LEVELS[level]
        
        # 总概率
        total_prob = attr_prob * count_prob * level_prob
        return total_prob
    
    @classmethod
    def calculate_value(cls, root_text):
        """计算灵根价值"""
        attributes, level = cls.split_root_text(root_text)
        # 获取概率
        probability = cls.calculate_probability(attributes, level)
        
        # 基础价值计算（概率越低，价值越高）
        base_value = math.pow(1 / probability, 0.5) * 100
        
        # 属性类型加成
        advanced_count = sum(1 for attr in attributes if attr in cls.ADVANCED_ATTRIBUTES)
        type_multiplier = 1 + (advanced_count * 0.5)  # 每个高级属性增加50%价值
        
        
        # 最终价值
        final_value = base_value * type_multiplier 
        
        return int(final_value)
    

    @classmethod
    def calculate_rarity_level(cls,root_text):
        value = cls.calculate_value(root_text)
        """计算稀有度等级"""
        if value >= 1000000:
            return "神话"
        elif value >= 100000:
            return "传说"
        elif value >= 10000:
            return "史诗"
        elif value >= 5000:
            return "稀有"
        elif value >= 1000:
            return "优秀"
        else:
            return "普通"

# 示例用法
def main():
    # 生成10000个灵根并统计价值分布
    roots = [SpiritRoot() for _ in range(10000)]
    
    # 输出最值钱的前5个灵根
    top_5 = sorted(roots, key=lambda x: x.value, reverse=True)[5000:5010]
    for root in top_5:
        print(f"灵根: {root.display_text(root.root_text)}")
        print(f"价值: {root.value}")
        print(f'修炼系数:{root.calculate_cultivation_coefficient(root.root_text)}')
        print(f"稀有度: {root.calculate_rarity_level(root.root_text)}")
        print("---")
    print('----最强灵根----')
    root_text = '金木风冰空-天'

    print(f"灵根: {SpiritRoot.display_text(root_text)}")
    print(f"价值: {SpiritRoot.calculate_value(root_text)}")
    print(f'修炼系数:{SpiritRoot.calculate_cultivation_coefficient(root_text)}')
    print(f"稀有度: {SpiritRoot.calculate_rarity_level(root_text)}")
    print("---")
