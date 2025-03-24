from utils import configure_logger
from dao.connectionPool import db_pool


from views.test_views.playerTest import main
# from utils.spiritroot import main

if __name__ == "__main__":
    configure_logger()  # 初始化日志系统
    
    # 初始化数据库连接池
    db_pool.initialize("dataset/zhetian3.db")
    
    try:
        main()
    finally:
        db_pool.close()
