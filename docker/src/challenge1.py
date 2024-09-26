import mysql.connector
import string
import random
import socket
from datetime import datetime
import threading
import os  

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'), 
            user=os.getenv('MYSQL_USER'), 
            password=os.getenv('MYSQL_PASSWORD'), 
            database=os.getenv('MYSQL_DB') 
        )
        print("Database connection successful")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def setup_challenge_table(challenge_id):
    table_name = f'challenge_{challenge_id}'
    connection = get_db_connection()
    
    if connection:
        try:
            cursor = connection.cursor()
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ip VARCHAR(255) NOT NULL,
                flag VARCHAR(255) NOT NULL,
                timestamp DATETIME NOT NULL
            );
            """
            cursor.execute(create_table_query)
            connection.commit()
            print(f"Table {table_name} created or already exists.")  
        except mysql.connector.Error as err:
            print(f"Error creating table {table_name}: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print(f"Error: No database connection for challenge_id {challenge_id}")
    
def genFlag():
    # Change this to generate a flag of your own
    # Format <FLAG> = "Flag{ChangeM3" + ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=25)) + "}" for 25 random characters (Uppercase, Lowercase, and Numbers)
    flag = "<FLAG>{" + ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=25)) + "}"
    return flag

def getFlagForIP(challenge_id, ip_address):
    table_name = f'challenge_{challenge_id}'
    connection = get_db_connection()

    if connection:
        cursor = connection.cursor()
        check_ip_query = f"SELECT flag FROM {table_name} WHERE ip = %s"
        cursor.execute(check_ip_query, (ip_address,))
        result = cursor.fetchone()

        if result:
            cursor.close()
            connection.close()
            return result[0] 

        flag = genFlag()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_flag_query = f"INSERT INTO {table_name} (ip, flag, timestamp) VALUES (%s, %s, %s)"
        cursor.execute(insert_flag_query, (ip_address, flag, timestamp))
        connection.commit()
        cursor.close()
        connection.close()

        return flag
    else:
        print(f"Error: No database connection for IP {ip_address}")
        return None

def getQuestions():
    # Change this questions
    questions = [
        {
            "question": "What is the capital of Indonesia?\nFormat: string\n> ",
            "correct_answer": "Jakarta"
        },
        {
            "question": "\n1+1=?\nFormat: number\n> ",
            "correct_answer": "2"
        },
        {
            "question": "\nWhat is the name of this image\nFormat: filename.extention\n> ",
            "correct_answer": "main.jpg"
        }
    ]
    return questions

def getTitleAndExitInfo(difficulty):
    # Change this title
    title = "\n\033[94m===== TITLE 1 =====\033[0m\n"

    if difficulty == 1:
        diff_color = "\033[92m"  
        difficulty_label = "Easy"
    elif difficulty == 2:
        diff_color = "\033[93m"  
        difficulty_label = "Medium"
    elif difficulty == 3:
        diff_color = "\033[91m"  
        difficulty_label = "Hard"
    else:
        diff_color = "\033[0m"  
        difficulty_label = "Unknown"
    
    diff_info = f"{diff_color}Difficulty: {difficulty_label}\033[0m\n"
    exit_info = "\033[93mNote: You can exit anytime by typing 'exit'\033[0m\n"
    return title, diff_info, exit_info


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address, challenge_id):
        self.connection = connection
        self.address = address
        self.challenge_id = challenge_id
        threading.Thread.__init__(self)

    def run(self):
        ip_address = self.address[0]
        flag = getFlagForIP(self.challenge_id, ip_address)
        
        if flag is None:
            self.connection.sendall("\033[91mError: Unable to fetch or generate flag.\033[0m\n".encode())
            self.connection.close()
            return
        
        questions = getQuestions()

        # Difficulty level set by the server (e.g., 1: easy, 2: medium, 3: hard)
        difficulty_level = 3

        title, diff_info, exit_info = getTitleAndExitInfo(difficulty_level)
        self.connection.sendall((title + diff_info + exit_info + "\n").encode())

        for question_data in questions:
            question = question_data["question"]
            correct_answer = question_data["correct_answer"]

            while True:
                try:
                    self.connection.sendall(question.encode())
                    response = self.connection.recv(128).decode().strip()

                    if response == "exit":
                        self.connection.sendall("\033[92mConnection closed\033[0m\n".encode())
                        self.connection.close()
                        return

                    if response == correct_answer:
                        break 
                    else:
                        self.connection.sendall("\033[91mWrong answer. Try again.\033[0m\n".encode())
                except OSError:
                    return 

        self.connection.sendall(f"\033[92mCongratulations! Here is your flag: {flag}\033[0m\n".encode())
        self.connection.close()

class Server(threading.Thread):
    def __init__(self, challenge_id):
        self.challenge_id = challenge_id
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        setup_challenge_table(self.challenge_id)
        # Change this port
        port = 10000
        self.my_socket.bind(('0.0.0.0', port))
        self.my_socket.listen(1)
        print(f"server is listening in {port}")
        while True:
            connection, client_address = self.my_socket.accept()
            clt = ProcessTheClient(connection, client_address, self.challenge_id)
            clt.start()
            self.the_clients.append(clt)

def main():
    # Change this challenge ID
    challenge_id = 1
    svr = Server(challenge_id)
    svr.start()

if __name__ == "__main__":
    main()