import string
import random
import socket
from datetime import datetime
import threading
import csv
import os

# Function to generate a unique flag
def genFlag():
    # Change this to generate a flag of your own
    # Format <FLAG> = "Flag{ChangeM3" + ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=25)) + "}" for 25 random characters (Uppercase, Lowercase, and Numbers)
    flag = "<FLAG>{" + ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=25)) + "}"
    return flag

# Check if the IP is already in db_soal1.csv and return the corresponding flag, or generate a new one if it's a new IP
def getFlagForIP(ip_address):
    # Database file
    file_name = 'db_q1.csv'
    
    # Initialize database if not exists
    if not os.path.exists(file_name):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['IP', 'Flag', 'Timestamp'])  # Add a Timestamp column
    
    # Check if the IP already has a flag
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            if row[0] == ip_address:
                return row[1]  # Return the flag if IP exists
    
    # If IP is new, generate and save a flag with a timestamp
    flag = genFlag()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ip_address, flag, timestamp])
    
    return flag

# Function to handle questions and answers
def getQuestions():
    questions = [
        {
            "question": "question_1?\nFormat: string_1\n> ",
            "correct_answer": "answer_1"
        },
        {
            "question": "\nquestion_2?\nFormat: 0\n> ",
            "correct_answer": "2"
        },
        {
            "question": "\nquestion_3?\nFormat: filename.extention\n> ",
            "correct_answer": "answer_3.jpg"
        }
    ]
    return questions

# Function to handle title, difficulty, and exit info
def getTitleAndExitInfo(difficulty):
    # Change this title
    title = "\n\033[94m===== TITLE =====\033[0m\n"

    # Assign color based on difficulty
    if difficulty == 1:
        diff_color = "\033[92m"  # Green for easy
        difficulty_label = "Easy"
    elif difficulty == 2:
        diff_color = "\033[93m"  # Yellow for medium
        difficulty_label = "Medium"
    elif difficulty == 3:
        diff_color = "\033[91m"  # Red for hard
        difficulty_label = "Hard"
    else:
        diff_color = "\033[0m"  # Default (no color)
        difficulty_label = "Unknown"
    
    # Difficulty info with color
    diff_info = f"{diff_color}Difficulty: {difficulty_label}\033[0m\n"
    exit_info = "\033[93mNote: You can exit anytime by typing 'exit'\033[0m\n"
    return title, diff_info, exit_info


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        ip_address = self.address[0]
        flag = getFlagForIP(ip_address)
        questions = getQuestions()

         # Difficulty level set by the server (e.g., 1: easy, 2: medium, 3: hard)
        difficulty_level = 2

        # Send title, difficulty, and exit information
        title, diff_info, exit_info = getTitleAndExitInfo(difficulty_level)
        self.connection.sendall((title + diff_info + exit_info + "\n").encode())

        # Start asking questions
        for question_data in questions:
            question = question_data["question"]
            correct_answer = question_data["correct_answer"]

            # Stay in the current question until the correct answer is provided or "exit" is received
            while True:
                try:
                    self.connection.sendall(question.encode())
                    response = self.connection.recv(128).decode().strip()

                    if response == "exit":
                        self.connection.sendall("\033[92mKoneksi ditutup.\033[0m\n".encode())
                        self.connection.close()
                        return  # End the session if user wants to exit

                    if response == correct_answer:
                        break  # Move to the next question
                    else:
                        self.connection.sendall("\033[91mJawaban salah\033[0m\n".encode())
                except OSError:
                    return  # Handle disconnection

        # After all questions are answered correctly
        self.connection.sendall(f"\033[92mBenar! Ini flag-mu: {flag}\033[0m\n".encode())
        self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        # Change this port
        port = 10000
        self.my_socket.bind(('0.0.0.0', port))
        self.my_socket.listen(1)
        print(f"server is listening in {port}")
        while True:
            connection, client_address = self.my_socket.accept()
            clt = ProcessTheClient(connection, client_address)
            clt.start()
            self.the_clients.append(clt)

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()
