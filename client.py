import socket 
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.0.10", 55555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NOME':
                client.send(nome.encode('utf-8'))
            else:
                print(message)
        
        except:
            print("Um erro ocorreu")
            client.close()
            break

def write():
    while True:
        message = f'{nome}: {input("")}'
        client.send(message.encode("utf-8"))

nome = input("Digite seu nome: ")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
