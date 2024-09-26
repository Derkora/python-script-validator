import mysql.connector
import time
import os  

def ensure_table_exists():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'), 
            user=os.getenv('MYSQL_USER'), 
            password=os.getenv('MYSQL_PASSWORD'), 
            database=os.getenv('MYSQL_DB') 
        )
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS debugger (
        );
        """
        cursor.execute(query)
        connection.commit()
        print("Table created successfully")
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def retry_create_table(retries=5, delay=5):
    for attempt in range(retries):
        try:
            ensure_table_exists()
            print(f"Table creation succeeded on attempt {attempt + 1}")
            return True
        except mysql.connector.Error as err:
            print(f"Attempt {attempt + 1} failed: {err}. Retrying in {delay} seconds...")
            time.sleep(delay)
    print(f"Failed to create table after {retries} attempts.")
    return False

if __name__ == "__main__":
    retry_create_table()