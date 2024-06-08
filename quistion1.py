import socket
import threading

# Bank account 
accounts = {
    "user1": {"password": "pass1", "balance": 1000},
    "user2": {"password": "pass2", "balance": 2000},
    "user3": {"password": "pass3", "balance": 3000}
}

# TCP server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
server_socket.listen(5)

def handle_client(conn, addr):
    print(f"New connection from {addr}")

    conn.send(b"Enter your username: ")
    username = conn.recv(1024).decode().strip()
    conn.send(b"Enter your password: ")
    password = conn.recv(1024).decode().strip()

    if username not in accounts or accounts[username]["password"] != password:
        conn.send(b"Invalid credentials. Disconnecting.")
        conn.close()
        return

   
    while True:
        conn.send(b"Enter your choice (balance/deposit/withdraw/exit): ")
        choice = conn.recv(1024).decode().strip()

        if choice == "balance":
            balance = accounts[username]["balance"]
            conn.send(f"Your current balance is: {balance}".encode())
        elif choice == "deposit":
            conn.send(b"Enter the amount to deposit: ")
            amount = int(conn.recv(1024).decode().strip())
            accounts[username]["balance"] += amount
            conn.send(f"Deposit successful. New balance: {accounts[username]['balance']}".encode())
        elif choice == "withdraw":
            conn.send(b"Enter the amount to withdraw: ")
            amount = int(conn.recv(1024).decode().strip())
            if amount > accounts[username]["balance"]:
                conn.send(b"Insufficient funds.")
            else:
                accounts[username]["balance"] -= amount
                conn.send(f"Withdrawal successful. New balance: {accounts[username]['balance']}".encode())
        elif choice == "exit":
            conn.send(f"Final balance: {accounts[username]['balance']}".encode())
            conn.close()
            print(f"Connection with {addr} closed")
            return
        else:
            conn.send(b"Invalid choice. Please try again.")

def start_server():
    print("Server is running...")
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start_server()