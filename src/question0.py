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
    #flag = "Flag{ChangeM3" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=50)) + "}"
    flag = "<FLAG>"
    return flag

# Check if the IP is already in db_soal1.csv and return the corresponding flag, or generate a new one if it's a new IP
def getFlagForIP(ip_address):
    # change this file name if you want
    file_name = '<database_question0.csv>'
    if not os.path.exists(file_name):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['IP', 'Flag'])  

    # Check if the IP already has a flag
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        next(reader, None)  
        for row in reader:
            if row[0] == ip_address:
                return row[1]

    # If IP is new, generate and save a flag
    flag = genFlag()
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ip_address, flag])
    return flag

# Function to handle questions and answers
def getQuestions():
    questions = [
        {
            "question": "question_1?\nFormat: string_1\n> ",
            "correct_answer": "answer_1"
        },
        {
            "question": "question_2?\nFormat: 0\n> ",
            "correct_answer": "2"
        },
        {
            "question": "question_3?\nFormat: filename.extention\n> ",
            "correct_answer": "answer_3.jpg"
        }
    ]
    return questions

# Function to handle title and exit info
def getTitleAndExitInfo():
    title = "\n\033[94m===== TITLE =====\033[0m\n"
    exit_info = "\033[93mNote: You can exit anytime by typing 'exit'\033[0m\n"
    return title, exit_info

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        ip_address = self.address[0]
        flag = getFlagForIP(ip_address)
        questions = getQuestions()

        # Send title and exit information
        title, exit_info = getTitleAndExitInfo()
        self.connection.sendall((title + exit_info + "\n").encode())

        # Start asking questions
        for question_data in questions:
            question = question_data["question"]
            correct_answer = question_data["correct_answer"]

            # Stay in the current question until the correct answer is provided or "exit" is received
            while True:
                try:
                    self.connection.sendall(question.encode())
                    response = self.connection.recv(32).decode().strip()

                    if response == "exit":
                        self.connection.sendall("\033[92mKoneksi ditutup.\033[0m\n".encode())
                        self.connection.close()
                        return  # End the session if user wants to exit

                    if response == correct_answer:
                        break  # Move to the next question
                    else:
                        self.connection.sendall("\033[91mJawaban salah\033[0m\n\n".encode())
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
        # Change this port if you want
        port = <PORT>
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
