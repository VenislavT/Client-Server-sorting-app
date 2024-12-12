import socket
import os
import time

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def client_handler():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))
    buffer = ""

    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            buffer += data 


            while "\n" in buffer:
                server_message, buffer = buffer.split("\n", 1)
                server_message = server_message.strip()

                if server_message.lower() == "disconnect":
                    clear_terminal()
                    print("Connection closed. You can start a new session or exit.")
                    return

                if server_message.lower() == "restart":
                    print("Restarting the process...")
                    time.sleep(1)
                    clear_terminal()
                    break
           
                if "Enter" in server_message:
                    print(server_message, end=" ")
                    client_input = input() 
                    client_socket.send(client_input.encode('utf-8'))
                    continue
                else:
                    print(server_message)
            

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()


if __name__ == "__main__":
    while True:
        option = input("To start a new session, press 'Enter' (type 'exit' to quit): ").strip().lower()

        if option == "exit":
            print("Exiting the program...")
            break

        elif option != "":
            print("INVALID INPUT. Press 'Enter' to start a new session (type 'exit' to quit).")
            continue 
        clear_terminal()
        client_handler()
