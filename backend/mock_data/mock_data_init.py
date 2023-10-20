from main import db_manager as dbm
from sqlalchemy import text

def read_sql_file(filename):
    with open (filename, 'r') as file:
        return file.read()

def execute_sql_file(filename):

    engine, conn, metadata = dbm.db_connect()

    commands = read_sql_file(filename).split(';')  # Split commands by ';'
    with engine.connect() as connection:
        for command in commands:
            # Skip executing empty command caused by the split
            if command.strip() == "":
                continue
            
            try:
                connection.execute(text(command))
            except Exception as e:
                print(f"Error executing command: {command.strip()}")
                print("Error message:", e)

    # commands = read_sql_file(filename)
    # # cursor = conn.cursor()
    # cursor = conn.execute(commands)
    # cursor.close()

