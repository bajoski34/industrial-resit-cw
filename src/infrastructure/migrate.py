import pymysql.cursors
import os

def execute_sql_file(cursor, file_path):
    with open(file_path, 'r') as file:
        sql = file.read()
        for statement in sql.split(';'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

def main():
    print(os.curdir)
    migration_dir = 'infrastructure/migrations'
    migration_files = sorted(
        [f for f in os.listdir(migration_dir) if f.endswith('.sql')],
        key=lambda x: x.split('_')[0]
    )

    connection = pymysql.connect(host='bk_mysql',
                             user='bk_store_admin',
                             password='admin',
                             database='bk_store',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        for migration_file in migration_files:
            file_path = os.path.join(migration_dir, migration_file)
            print(f"Executing migration: {file_path}")
            execute_sql_file(cursor, file_path)
            connection.commit()
            print(f"Migration {migration_file} executed successfully.")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()