import socket
import threading

host = '192.168.0.10'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nomes = []

def broadcast(message, sender_name):
    for cliente in clients:
        if cliente != sender_name:
            try:
                cliente.send(message)
            except:
                index = clients.index(cliente)
                nomes.remove(nomes[index])
                clients.remove(cliente)

def handle(client, nome):
    while True:
        try:
            message = client.recv(1024)
            if message:
                if message.decode('utf-8') == 'exit':  # Verificando a mensagem de saída
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    nome = nomes[index]
                    broadcast(f'{nome} saiu do servidor\n'.encode('utf-8'), "")
                    nomes.remove(nome)
                    break
                broadcast(message, nome)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nome = nomes[index]
            broadcast(f'{nome} saiu do servidor\n'.encode('utf-8'), "")
            nomes.remove(nome)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Conectando a {str(address)}")

        client.send("nome".encode('utf-8'))
        nome = client.recv(1024).decode('utf-8')
        nomes.append(nome)
        clients.append(client)

        print(f'Nome do cliente é {nome}!')
        broadcast(f'{nome} entrou no servidor\n'.encode('utf-8'), nome)
        client.send('conectado'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client, nome))
        thread.start()

print("Server carregando...")
receive()
