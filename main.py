from utils import configure_logger
import logging 
if __name__ == "__main__":
    configure_logger()  # 初始化日志系统
    logger = logging.getLogger(__name__)
    logger.info("Hello, World!")
    logger.debug("Hello, World!")