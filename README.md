# Документация за Клиент-Сървър архитуктура, която реализира паралелен Quick sort и Merge sort

Това приложение е клиент-сървър арихектура, която се занимава със сортиращите алгоритми QuickSort и MergeSort. При връзка между клиент и сървър, клиентът изпраща на сървъра списък с числа и получава от сървъра сортирания списък. Използва многонишков модел за обслужване на голяма бройка клиенти и се ползват паралелни модели на сортиранията.

## Структура на проекта
 - **server.py** - кодът на сървъра
 - **client.py** - кодът на клиента
 
 Сървърът се стартира с изпълнение на файлът **server.py**, а всеки от клиентите, за да се сврърже със сървъра трябва да стартира **client.py**.

## Сървърът

### Характеристики
1. **Обработка на клиенти:**

   - Поддържа множество клиенти чрез използване на нишки(threads).
   - Опции за приключване (exit) и за рестартиране (restart) на текуща сесия.
2. **Алгоритми за сортиране:**

    - Стандартен и многонишков Quick sort.
    - Стандартен и многонишков Merge sort.
3. **Обработка на грешки**
    - Валидира входът на потребителя за включване в сървъра, брой елементи, нишки и данни.
    - Обработва невалидните данни въведени от потребителя с подходящи съобщения за грешки.

### Основни компоненти

1. Стартиране на сървъра

2. Алгоритми за сортиране - merge sort, паралелен merge sort, quick sort, паралелен quick sort

3. Комуникация с клиента

 - ## main function
    **Main** функцията стартира сървъра като вика **start_server()**
 - ## start_server()
    **Start_server()** фунцкията стартира сървър, който може да обработва множество клиенти едновременно използвайки нишки (threads) за паралелна обработка.
    
    ### 1. Създаване на сокет
    
    ```python
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ```
    Създава се сокет със ```socket.socket()``` като ```socket.AF_INET``` e за **IPv4** адреси и ```socket.SOCK_STREAM``` e за **TCP** протокол.

    ### 2. Свързване на сокета към IP адрес и порт и слушане на връзки 
    ```python
    server.bind(('127.0.0.1', 8080))
    server.listen()
    ```
    Свързва сървъра към локалния адрес ```127.0.0.1``` и порт ```8080```. Подготвя сървъра за връзки от клиенти.

    ### 3. Обработка на клиенти
    ``` python
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
    ```
    ```accept()``` - блокира изпълнението, докато не се свърже клиент. При връзка ```client_socket``` е сокет за комуникация с клиентът, а ```addr``` е наредена двойка от **IP** адрес и **порт** на клиента.

    ```client_thread``` - създава нова нишка за всеки клиент, която изпълнява функцията ```handle_client()```. Предава сокета и адреса на клиента като аргументи към функцията.

    ### 4. Затваряне на сървъра
    ```python
    except KeyboardInterrupt:
        print("Shutting down the server...")
    finally:
        server.close()
    ```
    При натискане на ```Ctrl+C``` се хваща изключение **KeyboardInterrupt**. Сървърът се затваря чрез ```server.close()```.

- ## get_number_of_elements(client_socket)
    ### 1. Изпращане на съобщение и получаване на вход от клиентът
    ```python
    client_socket.send("\nEnter the number of elements:  \n".encode('utf-8'))
    num_elements_message = client_socket.recv(1024).decode('utf-8')
    ```
    Сървърът изпраща съобщение до клиента, за въвеждане на брой на елементите. След това сървърът получава вход от клиентът чрез сокета и го декодира в текстов формат.

    ### 2. Проверки за команди
    ```python
    if "exit" in num_elements_message.lower():
        client_socket.send("disconnect\n".encode('utf-8'))
        return None 
        
    if "restart" in num_elements_message.lower():
        client_socket.send("restart\n".encode('utf-8'))
        return "restart"
    ``` 
    Ако клиентът е въвел **exit** или **restart** се изпраща съобщение за конкретния случай като приключва функцията и връща при **exit** - ```None``` и при **restart** - ```restart```.

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

- ## get_elements(client_socket, num_elements):
    Изпращане на съобщение, получаване на вход от клиентът и проверките за команди са като при ```get_number_of_elements(client_socket)```. Единствената разлика е съобщението ```client_socket.send(f"Enter {num_elements} elements separated by spaces: \n".encode('utf-8'))``` и това че се чакат множество елементи.

    ### 1. Преобразуване на входа в списък от числа 
    ```python
    arr = list(map(int, data.split()))
    ```
    Преобразува входните данни в списък от цели числа. Ако преобразуването е неуспешно, се хвърля ```ValueError```.

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
    В тази функция се изпращат съобщенията, които са част от интефейса, който подобрява взаимодействието с клиента. ```i``` е булева променлива, която определя дали ще се изпратят съобщенията.
    ### 1. Изпращане на първо съобщение
    ```python
    client_socket.send("---Welcome to the sorting server!---\n".encode('utf-8'))
    ```
    Сървърът изпраща съобщение до клиента, като ```encode('utf-8')``` преобразува текста в байтов формат, необходим за изпращане през сокета.
    ### 2. Изпращане на второ съобщение
    ```python
    client_socket.send("Tip: You can type 'exit' at any time to disconnect, or 'restart' to start over.\n".encode('utf-8'))
    ```
    Сървърът информира клиента за наличните команди: ```exit``` за прекъсване на връзката. ```restart``` за рестартиране на сесията.

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

    Рекурсивно разделя масива на две половини, докато всяка част не съдържа само един елемент. Проверява дали списъкът съдържа 1 или 0 елемента (база на рекурсията).Разделя списъка на две части. Рекурсивно сортира всяка част. Използва ```merge```, за да обедини двете сортирани части в една.

   ### 2. merge:

    Обединява два сортирани списъка в един сортиран списък. Сравнява текущите елементи от двата списъка и добавя по-малкия към резултата. След минаване на последния индекс на един от списъците, добавя остатъка от другия.

- ## Parallel Merge sort
    ### 1. Сортиране на част от масива
    ```python
    def merge_sort_part(chunks, chunk_indx):
        chunks[chunk_indx] = merge_sort(chunks[chunk_indx])
    ```
    Извиква функцията ```merge_sort```, за да сортира част от масива, която е в ```chunks[chunk_indx]```.
    ### 2. Разделяне на масивър на части
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
    Изчислява размер на всяка част и създава списък от части, които ще бъдат сортирани паралелно.

    ### 3. Създаване и стартиране на нишки
    ```python
    threads = []

    for i in range(parts):
        thread = threading.Thread(target=merge_sort_part, args=(chunks, i))
        threads.append(thread)

    for i in threads:
        i.start()
    ```
    За всяка част от масива се създава нишка, която изпълнява функцията ```merge_sort_part```, за да сортира частта. След това всички нишки се стартират. След това се ползва ```i.join()``` за изчакване за завършване на нишките.

    ### 4. Обединяване на частите
    ```python
    result = chunks[0]
    for i in chunks[1:]:
        result = merge(result, i)

    return result
    ```
    Използва функцията ```merge``` за обединяване на всяка следваща част с текущия резултат, започвайки от първата част.

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
    Ако масивът съдържа 0 или 1 елемента, той вече е сортиран и се връща директно. В противен случай, избираме опорен елемент (```pivot```), който ще е средния елемент на масива. Масивът се разделя на три части: 
     - **left:** Елементи по-малки от ```pivot```. 
     - **right:** Елементи по-големи от ```pivot```. 
     - **middle:** Елементи, равни на ```pivot```. 
     
    Функцията рекурсивно сортира частите **left** и **right**, и обединява тях заедно с елементите от **middle**, за да получи окончателно сортирания масив.

- ## Parallel Quick sort
    Паралелния Quick sort е същият като **Parallel Merge sort**, където масивът се разбива на части, пускат се нишки, които сортират малките части и се обединяват с ```merge```.



    







        






