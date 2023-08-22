import socket
import threading
import time
import sys


class ChatClienteServidor:
    def __init__(self, servidorHost, servidorPorta, clienteHost, clientePorta):
        self.servidorHost = servidorHost
        self.servidorPorta = servidorPorta
        self.clienteHost = clienteHost
        self.clientePorta = clientePorta
        self.thread_servidor = threading.Thread(target=self.iniciar_servidor)
        self.thread_cliente = threading.Thread(target=self.iniciar_cliente)
        self.mensagemCliente=""
        self.mensagemServidor=""
        self.flagCliente = 0
        self.flagServidor = 0

    def conexaoAtiva():
        return True
    
    # def status_cliente(self):
    #     return self.flagCliente
    
    def set_cliente(self,mensagemCliente):
        self.mensagemCliente=mensagemCliente
        self.flagCliente=1

    def get_cliente(self): 
        self.flagCliente=0
        return self.mensagemCliente
    
    def set_servidor(self,mensagemServidor):
        self.mensagemServidor=mensagemServidor
        self.flagServidor=1

    def get_servidor(self): 
        self.flagServidor=0
        return self.mensagemServidor

    
    def tratar_cliente(self, socket_cliente):
        while True:
            try:
                dados = socket_cliente.recv(1024)
                if not dados:
                    break
                self.flagCliente = 1
                print(f"Cliente diz: {dados.decode('utf-8')}\n")
                self.set_cliente(dados.decode('utf-8'))
            except Exception as e:
                print(f"Erro na conexão: {e}")
                break
        socket_cliente.close()
    ##Recebimento de Mensagens
    def iniciar_servidor(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((self.servidorHost, self.servidorPorta))
        servidor.listen(5)
        print("Servidor aguardando conexões...")
        
        self.thread_cliente.start()  # Iniciar o cliente em uma thread separada

        while True:
            socket_cliente, endereco_cliente = servidor.accept()
            print(f"Conexão estabelecida com {endereco_cliente}\n")
            manipulador_cliente = threading.Thread(target=self.tratar_cliente, args=(socket_cliente,))
            manipulador_cliente.start()
    
    ##Envio de mensagens
    def iniciar_cliente(self):
        while True:
            try:
                time.sleep(1)
                cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                cliente.connect((self.clienteHost, self.clientePorta))  # Usar a porta do outro servidor
                print("Conexão estabelecida com o servidor.")
        
                while True:
                    try:
                        if self.flagServidor == True:
                            mensagem = self.get_servidor()
                            cliente.sendall(mensagem.encode('utf-8'))
                    except KeyboardInterrupt:
                        print("\nSaindo do chat.")
                        break
                    except Exception as e:
                        print(f"Erro na conexão: {e}")
                        break
        
                cliente.close()
        
            except Exception as e:
                print(f"Erro na conexão: {e}")
                print("Tentando novamente em 1 segundo...")
                time.sleep(1)


    def iniciar(self):
        self.thread_servidor.start()
    
    def desligar(self):
        self.thread_servidor.join()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python nome_do_arquivo.py servidorHost servidorPorta clienteHost clientePorta")
        sys.exit(1)
   
    servidorHost, servidorPorta, clienteHost, clientePorta = sys.argv[1],int(sys.argv[2]),sys.argv[3],int(sys.argv[4])

    chat = ChatClienteServidor(clienteHost, clientePorta,servidorHost, servidorPorta)
    chat.iniciar()
