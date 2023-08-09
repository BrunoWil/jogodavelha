import socket
import threading
import time

def tratar_cliente(socket_cliente):
    while True:
        try:
            dados = socket_cliente.recv(1024)
            if not dados:
                break
            print(f"Cliente diz: {dados.decode('utf-8')}\n")
        except Exception as e:
            print(f"Erro na conexão: {e}")
            break
    socket_cliente.close()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("localhost", 9990))
    servidor.listen(5)
    print("Servidor aguardando conexões...")
    thread_cliente.start()

    while True:
        socket_cliente, endereco_cliente = servidor.accept()
        print(f"Conexão estabelecida com {endereco_cliente}\n")
        manipulador_cliente = threading.Thread(target=tratar_cliente, args=(socket_cliente,))
        manipulador_cliente.start()

def iniciar_cliente():
    while True:
        try:
            # Cria um socket do tipo IPv4 e TCP
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Conecta o cliente ao endereço e porta do servidor
            cliente.connect(("localhost", 9999))  # Use a mesma porta do servidor: 9990
            print("Conexão estabelecida com o servidor.")

            while True:
                try:
                    mensagem = input("Você 2: ")
                    cliente.sendall(mensagem.encode('utf-8'))
                except KeyboardInterrupt:
                    print("\nSaindo do chat.")
                    break
                except Exception as e:
                    print(f"Erro na conexão: {e}")
                    break

            # Fecha o socket do cliente
            cliente.close()
        except Exception as e:
            print(f"Erro na conexão: {e}")
            print("Tentando novamente em 1 segundo...")
            time.sleep(1)


if __name__ == "__main__":
    thread_servidor = threading.Thread(target=iniciar_servidor)
    thread_cliente = threading.Thread(target=iniciar_cliente)
    thread_servidor.start()

