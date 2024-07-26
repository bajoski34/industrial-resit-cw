import pymysql.cursors
# Database connection settings

db_config = {
    'host': 'bk_mysql',
    'port': 3306,
    'user': 'bk_store_admin',
    'password': 'admin',
    'database': 'bk_store'
}

connection = pymysql.connect(host=db_config['host'],
                             user=db_config['user'],
                             password=db_config['password'],
                             database=db_config['database'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
