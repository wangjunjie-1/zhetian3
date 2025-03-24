import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def configure_logger():
    # 从环境变量获取日志级别，默认为 INFO
    log_level_str = os.getenv('LOG_LEVEL', 'INFO')
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    
    # 创建根日志器
    logger = logging.getLogger()
    logger.setLevel(log_level)  # 使用环境变量中的日志级别

    # 通用日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 控制台Handler（使用环境变量中的日志级别）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # 文件Handler（使用环境变量中的日志级别）
    file_handler = RotatingFileHandler(
        'game.log',
        maxBytes=1024*1024*5,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger