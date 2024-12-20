# Документация за Клиент-Сървър архитeктура, която реализира паралелен Quick sort и Merge sort

Това приложение е клиент-сървър архитектура, която се занимава със сортиращите алгоритми Quick sort и Merge sort. При връзка между клиент и сървър, клиентът изпраща на сървъра списък с числа и получава от сървъра сортирания списък. Използва многонишков модел за обслужване на голяма бройка клиенти и се ползват паралелни модели на сортиранията.

## Съдържание
- [Изисквания](#изисквания)
- [Структура на архитектурата](#структура-на-архитектурата)
- [Сървър](#сървър)
    - [main()](#main-function)
    - [start_server()](#start_server)
    - [get_number_of_elements()](#get_number_of_elementsclient_socket)
    - [get_number_of_threads()](#get_number_of_threadsclient_socket)
    - [get_elements()](#get_elementsclient_socket-num_elements)
    - [general_messages()](#general_messagesclient_socketi)
    - [merge_sort()](#merge-sort)
    - [parallel_merge_sort()](#parallel-merge-sort)
    - [quick_sort()](#quick-sort)
    - [parallel_quick_sort()](#parallel-quick-sort)
    - [handle_client()](#handle_clientclient_socket-addr)
- [Клиент](#клиент)
    - [main()](#main-function-1)
    - [clear_terminal()](#def-clear_terminal---изчистване-на-терминала)
    - [client_handler()](#client_handler)
- [Инсталация](#инсталация)
- [Стартиране](#стартиране)
- [Настройки за мрежата](#настройки-за-мрежата)
- [Тестване](#тестване)

## Изисквания
- Python 3.7 или по-нова версия
- Вградени библиотеки:
  - `socket`
  - `threading`
  - `time`
  - `os`

## Структура на архитектурата
 - **server.py** - кодът на сървъра
 - **client.py** - кодът на клиента
 
 Сървърът се стартира с изпълнение на файлът **server.py**, а всеки от клиентите, за да се свърже със сървъра, трябва да стартира **client.py**.

## Сървър

### Характеристики
1. **Обработка на клиенти:**
   - Поддържа множество клиенти чрез използването на нишки(**threads**).
   - Опции за приключване (**exit**) и за рестартиране (**restart**) на текуща сесия.
2. **Алгоритми за сортиране:**
    - Стандартен и многонишков Quick sort.
    - Стандартен и многонишков Merge sort.
3. **Обработка на грешки**
    - Валидира входа на потребителя за включване в сървъра, брой елементи, нишки и данни.
    - Обработва невалидните данни въведени от потребителя с подходящи съобщения за грешки.

### Основни компоненти

1. Стартиране на сървъра

2. Алгоритми за сортиране - merge sort, паралелен merge sort, quick sort, паралелен quick sort

3. Комуникация с клиента

 - ## main function
    **Main** функцията стартира сървъра като вика **start_server()**
 - ## start_server()
    **Start_server()** функцията стартира сървър, който може да обработва множество клиенти едновременно използвайки нишки (threads) за паралелна обработка.
    
    ### 1. Създаване на сокет
    
    ```python
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ```
    Създава се сокет със `socket.socket()` като `socket.AF_INET` e за **IPv4** адреси и `socket.SOCK_STREAM` e за **TCP** протокол.

    ### 2. Свързване на сокета към IP адрес и порт и слушане на връзки 
    ```python
    server.bind(('127.0.0.1', 8080))
    server.listen()
    ```
    Свързва сървъра към локалния адрес `127.0.0.1` и порт `8080`. Подготвя сървъра за връзки от клиенти.

    ### 3. Обработка на клиенти
    ``` python
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
    ```
    `accept()` - блокира изпълнението, докато не се свърже клиент. При връзка `client_socket` е сокет за комуникация с клиентът, а `addr` е наредена двойка от **IP** адрес и **порт** на клиента.

    `client_thread` - създава нова нишка за всеки клиент, която изпълнява функцията `handle_client()`. Предава сокета и адреса на клиента като аргументи към функцията.

    ### 4. Затваряне на сървъра
    ```python
    except KeyboardInterrupt:
        print("Shutting down the server...")
    finally:
        server.close()
    ```
    При натискане на **Ctrl+C** се хваща изключение **KeyboardInterrupt**. Сървърът се затваря чрез `server.close()`.

- ## get_number_of_elements(client_socket)
    ### 1. Изпращане на съобщение и получаване на вход от клиента
    ```python
    client_socket.send("\nEnter the number of elements:  \n".encode('utf-8'))
    num_elements_message = client_socket.recv(1024).decode('utf-8')
    ```
    Сървърът изпраща съобщение до клиента, за въвеждане на брой на елементите. След това сървърът получава вход от клиента чрез сокета и го декодира в текстов формат.

    ### 2. Проверки за команди
    ```python
    if "exit" in num_elements_message.lower():
        client_socket.send("disconnect\n".encode('utf-8'))
        return None 
        
    if "restart" in num_elements_message.lower():
        client_socket.send("restart\n".encode('utf-8'))
        return "restart"
    ``` 
    Ако клиентът е въвел **exit** или **restart** се изпраща съобщение за конкретния случай като приключва функцията и връща при **exit** - `None` и при **restart** - `restart`.

    ### 3. Обработване на входа
    ```python
    num_elements = int(num_elements_message)
    ``` 
    Опит за преобразуване на входа в цяло число.

    ```python
    client_socket.send("Invalid number of elements. Please correct number of elements!\n".encode('utf-8'))
    continue
    ```
    Ако възникне грешка (невалиден вход), изпраща съобщение за грешка до клиента и клиентът може да опита отново да въведе брой числа.

- ## get_number_of_threads(client_socket):
    Функцията е като `get_number_of_elements(client_socket)`, но с една допълнителна проверка:
    ```python
    if num_threads > 0:
        return num_threads
    else:
        client_socket.send("Please type a positive number for threads.\n".encode('utf-8'))
        continue
    ```
    Преди грешката за невалиден вход, има проверка дали числото е отрицателно, за да се даде по-конкретно съобщение.

- ## get_elements(client_socket, num_elements):
    Изпращането на съобщения, получаването на входни данни от клиента и проверките за команди са като при `get_number_of_elements(client_socket)`. Единствената разлика е съобщението `client_socket.send(f"Enter {num_elements} elements separated by spaces: \n".encode('utf-8'))` и това че се чакат множество елементи.

    ### 1. Преобразуване на входа в списък от числа 
    ```python
    arr = list(map(int, data.split()))
    ```
    Преобразува входните данни в списък от цели числа. Ако преобразуването е неуспешно, се хвърля `ValueError`.

    ### 2. Проверка за брой елементи
    ```python
    if len(arr) != num_elements:
        client_socket.send(f"Expected {num_elements} elements. Try again.\n".encode('utf-8'))
        continue
    ```
    Проверява дали броят на въведените елементи съвпада с очаквания и ако не съвпада, клиентът може да опита отново да въведе правилен брой числа.
    ### 3. Обработка на грешни входни данни
    ```python
    except ValueError:
        client_socket.send("Invalid elements. Numbers only!\n".encode('utf-8'))
        continue
    ``` 
    При грешни входни данни се изпраща съобщение и клиентът може да опита отново да въведе правилни числа.

- ## general_messages(client_socket,i):
    В тази функция се изпращат съобщенията, които са част от интефейса, който подобрява взаимодействието с клиента. `i` е булева променлива, която определя дали ще се изпратят съобщенията.
    ### 1. Изпращане на първо съобщение
    ```python
    client_socket.send("---Welcome to the sorting server!---\n".encode('utf-8'))
    ```
    Сървърът изпраща съобщение до клиента, като `encode('utf-8')` преобразува текста в байтов формат, необходим за изпращане през сокета.
    ### 2. Изпращане на второ съобщение
    ```python
    client_socket.send("Tip: You can type 'exit' at any time to disconnect, or 'restart' to start over.\n".encode('utf-8'))
    ```
    Сървърът информира клиента за наличните команди: `exit` за прекъсване на връзката. `restart` за рестартиране на сесията.

- ## Merge sort
    ```python
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
    ```
    ### 1. merge_sort(arr):

    Рекурсивно разделя масива на две половини, докато всяка част не съдържа само един елемент. Проверява дали списъкът съдържа 1 или 0 елемента (база на рекурсията). Разделя списъка на две части. Рекурсивно сортира всяка част. Използва `merge`, за да обедини двете сортирани части в една.

   ### 2. merge:

    Обединява два сортирани списъка в един сортиран списък. Сравнява текущите елементи от двата списъка и добавя по-малкия към резултата. След като премине през последния индекс на някой от списъците, добавя остатъка от другия.

- ## Parallel Merge sort
    ### 1. Сортиране на част от масива
    ```python
    def merge_sort_part(chunks, chunk_indx):
        chunks[chunk_indx] = merge_sort(chunks[chunk_indx])
    ```
    Извиква функцията `merge_sort`, за да сортира част от масива, която е в `chunks[chunk_indx]`.
    ### 2. Разделяне на масива на части
    ```python
    chunk_size = len(arr) // parts
    chunks = []

    for i in range(parts):
        start = i * chunk_size
        if i < parts - 1:
            end = (i + 1) * chunk_size
        else:
            end = len(arr)
        chunks.append(arr[start:end])
    ```
    Изчислява размера на всяка част и създава списък от части, които ще бъдат сортирани паралелно.

    ### 3. Създаване и стартиране на нишки
    ```python
    threads = []

    for i in range(parts):
        thread = threading.Thread(target=merge_sort_part, args=(chunks, i))
        threads.append(thread)

    for i in threads:
        i.start()

    for i in threads:
        i.join()
    ```
    За всяка част от масива се създава нишка, която изпълнява функцията `merge_sort_part`, за да сортира частта. След това всички нишки се стартират. Ползва се `i.join()` за изчакване за завършването на нишките.

    ### 4. Обединяване на частите
    ```python
    result = chunks[0]
    for i in chunks[1:]:
        result = merge(result, i)

    return result
    ```
    Използва функцията `merge` за да обедини всяка следваща част с текущия резултат, започвайки от първата част.

- ## Quick sort
    ```python
    def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [num for num in arr if num < pivot]
        right = [num for num in arr if num > pivot]
        middle = [num for num in arr if num == pivot]
        return quick_sort(left) + middle + quick_sort(right)
    ```
    Ако масивът съдържа 0 или 1 елемента, той вече е сортиран и се връща директно. В противен случай, избираме опорен елемент (**pivot**), който в този случай ще е средния елемент на масива. Масивът се разделя на три части: 
     - **left:** Елементи по-малки от **pivot**. 
     - **right:** Елементи по-големи от **pivot**. 
     - **middle:** Елементи, равни на **pivot**. 
     
    Функцията рекурсивно сортира частите **left** и **right**, и обединява тях заедно с елементите от **middle**, за да получи окончателно сортирания масив.

- ## Parallel Quick sort
    Паралелния Quick sort е същият като **Parallel Merge sort**, където масивът се разбива на части, пускат се нишки, които сортират малките части и се обединяват с `merge`.
- ## handle_client(client_socket, addr)
    Тази функция обработва заявките на клиент, като получава данни от клиента, извършва различни сортировки (нормална и многонишкова за `Merge Sort` и `Quick Sort`), и връща резултати и времето на изпълнение обратно на клиента.

    ### 1. Изпращане на интерфейсът
    ```python
    general_messages(client_socket, general_messages_bool)
    general_messages_bool = False
    ```
    Функцията започва с изпращане на съобщения към клиента чрез `general_messages`. Те са в `while` цикълът, защото трябва да се изпратят отново при рестартиране на интефейса.

    ### 2. Обработване на брой числа и елементи
    ```python
    num_elements = get_number_of_elements(client_socket)
    if num_elements is None: 
        break
    if num_elements == "restart":
        general_messages_bool = True
        continue
    ```
    Получава се броят на елементите, които ще бъдат сортирани чрез `get_number_of_elements()` и числата чрез `get_elements()`. Двете функции връщат правилно число/числа или `None` или `restart`. `None` и `restart` се връщат, защото клиентът е въвел `exit` или `restart`. След това се правят 2 проверки, при `None`(от `exit`) се затваря връзката на клиента със сървъра, а при `restart`(от `restart`) се рестартира интерфейсът.

    ### 3. Сортирания на получените числа
    ```python
    start = time.perf_counter()
    arr = merge_sort(arr)
    client_socket.send(f"\n---Single-thread merge sort: {arr}\n".encode('utf-8'))
    end = time.perf_counter()
    client_socket.send(f"The function took {(end-start):.15f} seconds.\n".encode('utf-8'))
    time.sleep(0.01)
    ```
    Извършват се сортирания с различни алгоритми:
       
    1. Single-thread Merge Sort
    2. Multi-thread Merge Sort
    3. Single-thread Quick Sort
    4. Multi-thread Quick Sort

    Всеки резултат от сортирането се изпраща обратно на клиента заедно с времето на изпълнение. Ползва се `arr = arr_original` за възстановяване на първоначалния масив, преди всяко сортиране.

    ### 4. Затваряне на сокет
    ```python
    print(f"Client {addr[0]}:{addr[1]} disconnected.")
    client_socket.close()
    ```
    Когато всички задачи бъдат обработени или ако клиентът се изключи, сокетът се затваря и връзката с клиента се прекратява.

## Клиент
### Характеристики

1. **Клиент-сървър комуникация**: Използва сокети за обмен на данни.
2. **Управление на съобщения**: Анализира съобщения от сървъра и предприема съответните действия.
3. **Изчистване на ресурси**: Гарантира, че сокетът се затваря коректно, дори при грешки.

### Основни компоненти
 - ## main function
    ### 1. Получаване на потребителски вход

    ```python
    option = input("To start a new session, press 'Enter' (type 'exit' to quit): ").strip().lower()
    ```
    Входът се почиства от излишни интервали и се преобразува в малки букви за по-лесна обработка.

    ### 2. Обработване на входните данни

    ```python
    if option == "exit":
        print("Exiting the program...")
        break

    elif option != "":
        print("INVALID INPUT. Press 'Enter' to start a new session (type 'exit' to quit).")
        continue 

    ```
    Ако входните данни са `exit`, то извежда съобщение за излизане и прекъсва цикъла с `break`. Другата проверка е за въведен невалиден вход (например текст, различен от `exit`). Извежда съобщение за грешка и продължава към следващата итерация с `continue`.

    ### 3. Стартиране на нова сесия:
    ```python
    clear_terminal()
    client_handler()
    ```
    Изчиства терминала и стартира функцията `client_handler()` за работа с клиентския сокет.

 - ## def clear_terminal() - изчистване на терминала

    ```python
    def clear_terminal():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    ```
    Изчиства терминала в зависимост от операционната система. Ако системата е **Windows** `(os.name == 'nt')`, се извиква командата `cls` за изчистване. За други операционни системи, като **Linux** или **macOS**, се използва командата `clear`.
 - ## client_handler()
    ### 1. Създаване на сокет

    ```python
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))
    ```
    Създава **TCP** сокет `(socket.AF_INET, socket.SOCK_STREAM)` за връзка с локален сървър **(127.0.0.1)** на порт **8080**.

    ### 2.Обработка на съобщения от сървъра
    ```python
    data = client_socket.recv(1024).decode('utf-8')
    buffer += data
    while "\n" in buffer:
        server_message, buffer = buffer.split("\n", 1)
        server_message = server_message.strip()
    ```
    Получават се до **1024** байта данни и се декодират като текст чрез `recv` и `decode`. Данните се добавят към `buffer`, тъй като може да не се получат наведнъж. Разделя се `buffer` на 2 части: съобщението от сървъра и остатъка от данните. Премахва излишни интервали чрез `strip()`.
    ### 3. Различни типове съобщения
    - **Прекъсване на връзката**:

        ```python
        if server_message.lower() == "disconnect":
            clear_terminal()
            print("Connection closed. You can start a new session or exit.")
            return
        ```
        Затваря връзката и информира потребителя. Ако съобщението е `disconnect`, изчиства терминала и излиза от функцията.

    - **Рестартиране на процеса**:

        ```python
        if server_message.lower() == "restart":
            print("Restarting the process...")
            time.sleep(1)
            clear_terminal()
            break
        ```
        Изпълнява рестарт. Изчиства терминала след кратко изчакване, за да покаже че се изпълнява рестартирането и излиза от текущия цикъл.

    - **Въвеждане от потребителя**:

        ```python
        if "Enter" in server_message:
            print(server_message, end=" ")
            client_input = input() 
            client_socket.send(client_input.encode('utf-8'))
            continue
        ```
        Приема вход от потребителя и го изпраща на сървъра. Отпечатва съобщението от сървъра и чака потребителят да въведе отговор на същия ред.
    
    - **Нормални съобщения**:

        ```python
        else:
            print(server_message)
        ````
        Отпечатва съобщение, което не изисква действие.
    ### 4. Грешки и изчистване на ресурси:
    
    ```python
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
    ```
    Обработва грешки и гарантира, че сокетът е затворен. При грешка отпечатва съобщение за нея. Във `finally` сокетът се затваря, за да освободи ресурси.
    

## Инсталация

1. **Инсталиране на Python**
   - Уверете се, че Python е инсталиран:
     ```bash
     python --version
     # Или
     python3 --version
     ```
   - Ако не е, инсталирайте от [официалния сайт](https://www.python.org) или чрез пакетен мениджър (за Linux/MacOS).

2. **Клониране на проекта**
   - Клонирайте репозиторито или изтеглете файловете:
     ```bash
     git clone https://github.com/VenislavT/Client-Server-sorting-app.git
     cd <PROJECT_DIRECTORY>
     ```

3. **Създаване на виртуална среда**
   - Създайте и активирайте виртуална среда:
     ```bash
     python -m venv venv
     # Windows
     venv\Scripts\activate
     # Linux/MacOS
     source venv/bin/activate
     ```

4. **Инсталиране на зависимости**
   - Проектът няма външни зависимости. Уверете се, че виртуалната среда е активирана.
## Стартиране

### Стартиране на сървъра
1. Отворете терминал.
2. Стартирайте сървъра:
   ```bash
   python server.py
   # Или
   python3 server.py
   ```

### Стартиране на клиента
1. Отворете втори терминал.
2. Стартирайте клиента:

   ```bash
   python client.py
   # Или
   python3 client.py
   ```
## Настройки за мрежата
Ако клиентът и сървърът са на различни машини:
1. Променете IP адреса в `client.py` и `server.py`:

   ```python
   client_socket.connect(('SERVER_IP_ADDRESS', 8080))
   ```
   ```python
   server.bind(('SERVER_IP_ADDRESS', 8080))
    ```
2. Уверете се, че портът `8080` е отворен и видим през мрежата.






    







        






