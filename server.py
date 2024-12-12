
import socket
import threading
import time

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    middle = len(arr) // 2
    left = merge_sort(arr[:middle])
    right = merge_sort(arr[middle:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i+=1
        else:
            result.append(right[j])
            j+=1

    result = result + left[i:] + right[j:]

    return result

def merge_sort_part(chunks, chunk_indx):
    chunks[chunk_indx] = merge_sort(chunks[chunk_indx])

def parallel_merge_sort(arr, parts=2):
    if len(arr) <= 1:
        return arr

    chunk_size = len(arr) // parts
    chunks = []

    for i in range(parts):
        start = i * chunk_size

        if i < parts - 1:
            end = (i + 1) * chunk_size
        else:
            end = len(arr)

        chunks.append(arr[start:end])
    
    threads = []

    for i in range(parts):
        thread = threading.Thread(target=merge_sort_part, args=(chunks, i))
        threads.append(thread)

    for i in threads:
        i.start()

    for i in threads:
        i.join()

    result = chunks[0]
    for i in chunks[1:]:
        result = merge(result, i)
    
    return result

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [num for num in arr if num < pivot]
        right = [num for num in arr if num > pivot]
        middle = [num for num in arr if num == pivot]
        return quick_sort(left) + middle + quick_sort(right)
    
def quick_sort_part(chunks, chunk_indx):
    chunks[chunk_indx] = quick_sort(chunks[chunk_indx])

def parallel_quick_sort(arr, parts=2):
    if len(arr) <= 1:
        return arr

    chunk_size = len(arr) // parts
    chunks = []

    for i in range(parts):
        start = i * chunk_size

        if i < parts - 1:
            end = (i + 1) * chunk_size
        else:
            end = len(arr)

        chunks.append(arr[start:end])
    
    threads = []

    for i in range(parts):
        thread = threading.Thread(target=quick_sort_part, args=(chunks, i))
        threads.append(thread)

    for i in threads:
        i.start()

    for i in threads:
        i.join()

    result = chunks[0]
    for i in chunks[1:]:
        result = merge(result, i)

    return result

def general_messages(client_socket,i):
    if i:
        client_socket.send("---Welcome to the sorting server!---\n".encode('utf-8'))
        time.sleep(0.01)
        client_socket.send("Tip: You can type 'exit' at any time to disconnect, or 'restart' to start over.\n".encode('utf-8'))
        time.sleep(0.01)


def get_number_of_elements(client_socket):
    while True:
        client_socket.send("\nEnter the number of elements:  \n".encode('utf-8'))
        num_elements_message = client_socket.recv(1024).decode('utf-8')

        if "exit" in num_elements_message.lower():
            client_socket.send("disconnect\n".encode('utf-8'))
            return None 
        
        if "restart" in num_elements_message.lower():
            client_socket.send("restart\n".encode('utf-8'))
            return "restart"

        try:
            num_elements = int(num_elements_message)
            return num_elements
        except ValueError:
            client_socket.send("Invalid number of elements. Please correct number of elements!\n".encode('utf-8'))
            continue

def get_elements(client_socket, num_elements):
    while True:
        try:
            client_socket.send(f"Enter {num_elements} elements separated by spaces: \n".encode('utf-8'))
            data = client_socket.recv(1024).decode('utf-8')

            if "restart" in data.lower():
                client_socket.send("restart\n".encode('utf-8'))
                return "restart"
            
            if "exit" in data.lower():
                client_socket.send("disconnect\n".encode('utf-8'))
                return None 
            
            arr = list(map(int, data.split())) 

            if len(arr) != num_elements:
                client_socket.send(f"Expected {num_elements} elements. Try again.\n".encode('utf-8'))
                continue 

            return arr 

        except ValueError:
            client_socket.send("Invalid elements. Numbers only!\n".encode('utf-8'))
            continue

def handle_client(client_socket, addr):
    general_messages_bool = True

    while True:
        general_messages(client_socket, general_messages_bool)
        general_messages_bool = False

        num_elements = get_number_of_elements(client_socket)

        if num_elements is None: 
            break

        if num_elements == "restart":
            general_messages_bool = True
            continue

        arr = get_elements(client_socket, num_elements)
        
        if arr is None:
            break

        if arr == "restart":
            general_messages_bool = True
            continue
        
        arr_original = arr.copy()

        print(f"Sorting of unsorted list {arr} for client {addr[0]}:{addr[1]}...")

        #Merge sort: single-thread
        start = time.perf_counter()
        arr = merge_sort(arr)
        client_socket.send(f"\n---Single-thread merge sort: {arr}\n".encode('utf-8'))
        end = time.perf_counter()
        client_socket.send(f"The function took {(end-start):.15f} seconds.\n".encode('utf-8'))
        time.sleep(0.01)

        #Merge sort: multi-threaded
        arr = arr_original

        start = time.perf_counter()
        arr = parallel_merge_sort(arr)
        client_socket.send(f"\n---Multi-threaded merge sort: {arr}\n".encode('utf-8'))
        end = time.perf_counter()
        client_socket.send(f"The function took {(end-start):.15f} seconds.\n".encode('utf-8'))
        time.sleep(0.01)

        #Quick sort: single-thread
        arr = arr_original
        
        start = time.perf_counter()
        arr = quick_sort(arr)
        client_socket.send(f"\n---Single-threaded quick sort: {arr}\n".encode('utf-8'))
        end = time.perf_counter()
        client_socket.send(f"The function took {(end-start):.15f} seconds.\n".encode('utf-8'))
        time.sleep(0.01)

        #Quick sort: multi-threaded
        arr = arr_original
        
        start = time.perf_counter()
        arr = parallel_quick_sort(arr)
        client_socket.send(f"\n---Multi-threaded quick sort: {arr}\n".encode('utf-8'))
        end = time.perf_counter()
        client_socket.send(f"The function took {(end-start):.15f} seconds.\n".encode('utf-8'))
        time.sleep(0.01)

    print(f"Client {addr[0]}:{addr[1]} disconnected.")
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8080))
    server.listen()
    print("Server is running on port 8080...")

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")

            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()

    except KeyboardInterrupt:
        print("Shutting down the server...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
