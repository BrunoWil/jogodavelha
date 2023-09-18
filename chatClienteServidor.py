import threading
import socket
import time

class ChatClienteServidor:
    def __init__(self, clienteHost, clientePorta, servidorHost, servidorPorta):
        self.servidorHost = servidorHost
        self.servidorPorta = servidorPorta
        self.clienteHost = clienteHost
        self.clientePorta = clientePorta
        self.mensagemCliente = ""
        self.mensagemServidor = ""
        self.servidorStatus=threading.Event()
        self.flagCliente = threading.Event()
        self.flagServidor = threading.Event()
        self.flagThreadInicial = threading.Event()
        self.flagThreadServidor = threading.Event()
        self.flagThreadCliente = threading.Event()
        self.flagThreadCliente.set()

    def set_cliente(self, mensagemCliente):
        self.mensagemCliente = mensagemCliente
        self.flagCliente.set()

    def get_cliente(self):
        self.flagCliente.clear()
        return self.mensagemCliente

    def set_servidor(self, mensagemServidor):
        self.mensagemServidor = mensagemServidor
        self.flagServidor.set()

    def get_servidor(self):
        self.flagServidor.clear()
        return self.mensagemServidor

    # def tratar_cliente(self, socket_cliente, mensagem):
    #     while True:
    #         try:
    #             if self.flagThreadCliente.is_set():
    #                 dados = socket_cliente.recv(1024)
    #                 if not dados:
    #                     break
    #                 mensagem = f"Usuario: {dados.decode('utf-8')}"
    #                 return mensagem
    #                 # self.exibicao_chat.insert(tk.END, mensagem + '\n')
    #         except Exception as e:
    #             print(f"Erro na conexão: {e}")
    #             break
    #     socket_cliente.close()

    def iniciar_servidor(self):
        try:
            self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.servidor.bind((self.servidorHost, self.servidorPorta))
            self.servidor.listen(2)
            print("Servidor aguardando conexões...")
        except:
            print("Host ou Porta Inválida...")

        while True:
            if not self.flagThreadInicial.is_set():
                break
            try:
                self.socket_cliente, endereco_cliente = self.servidor.accept()
                print(f"Conexão estabelecida com {endereco_cliente}\n")
                self.flagThreadServidor.set()
            except:
                print("Falha de Conexão")

    def iniciar_cliente(self):
        while True:
            if not self.flagThreadCliente.is_set():
                break
            try:
                time.sleep(1)
                self.cliente = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                
                self.cliente.connect((self.clienteHost, self.clientePorta))
                print("Conexão estabelecida com o servidor.")
                self.servidorStatus.set()
                break
            except Exception as e:
                print(f"Erro na conexão: {e}")
                print("Tentando novamente em 1 segundo...")
                time.sleep(1)

    def enviar_mensagens(self):
        try:

            mensagem = self.get_cliente()
            if mensagem:
                self.cliente.sendall(mensagem.encode('utf-8'))
                print(f"Você: {mensagem}")
                self.mensagemCliente=""
                return
        except KeyboardInterrupt:
            print("\nSaindo do chat.")
        except Exception as e:
            print(f"Erro na conexão: {e}")
            self.cliente.close()


    def iniciar(self):
        self.flagThreadInicial.set()
        self.thread_servidor = threading.Thread(target=self.iniciar_servidor)
        self.thread_servidor.start()
        thread_cliente = threading.Thread(target=self.iniciar_cliente,)
        thread_cliente.start()
        self.flagThreadCliente.set()


    def fecharConexao(self):
        self.servidor.close()