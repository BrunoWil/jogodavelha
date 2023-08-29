import sys
import time
import tkinter as tk
from tkinter import messagebox
import threading
import socket
from tkinter import scrolledtext, END
import json


class MeuAplicativoUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Meu Aplicativo")
        self.portaht=1059
        # Definir o tamanho da tela (largura x altura)
        self.geometry("220x280")

        # Criar widgets

        # Criar um frame para os widgets iniciais
        self.frameInicial = tk.Frame(self, borderwidth=2, relief="groove")
        self.frameInicial.grid(row=0, column=0, padx=10, pady=10)

        # Chamar os métodos para criar e posicionar os widgets
        self.criar_widgets()
        self.grid_caixa_inicial()

        # Dicionário para armazenar valores de host e porta
        self.host_porta = {"Porta", "Host"}
        self.mensagemServidor = ""
        self.protocol("WM_DELETE_WINDOW", self.desligar)
        self.estutura_mensagems={
        "Jogada":{},
        "Mensagem":{},
        "Estado_Vencedor":{}
        }
        self.gerenteTelas=threading.Event()
        thread_estados = threading.Thread(target=self.estadosDeTelas)
        self.gerenteTelas.set()
        thread_estados.start()



    def criar_widgets(self):
        # Definir mensagens padrão
        self.descricoes = {
            "Host": "Host:",
            "Porta": "Porta:",
            "Conectando": "Conectando"
        }

        # Obter informações de host local e porta local

        self.hostLocalMensagem = f"Host Local: {self.descobri_local_ip()}"
        self.portaLocalMensagem = f"Porta Local: {self.encontrar_portas_disponiveis(self.portaht, 47808)}"
        self.hostLocal = self.descobri_local_ip()
        self.portaLocal = self.encontrar_portas_disponiveis(self.portaht, 47808)

        # Criar dicionário para armazenar widgets
        self.widgets = {
            "labels": {},
            "entries": {},
            "buttons": {}
        }

        # Carregar frames para animação
        self.frameCnt = 12
        self.frames = [tk.PhotoImage(file='carregando.gif', format='gif -index %i' %
                                     i).subsample(50, 50) for i in range(self.frameCnt)]

        # Criar rótulos, caixas de texto e botão
        self.frame_caixa_inicial()

    def frame_caixa_inicial(self):
        # Criar e posicionar widgets usando o método grid
        self.widgets["labels"]["Host"] = tk.Label(
            self.frameInicial, text=self.descricoes["Host"])
        self.widgets["labels"]["Porta"] = tk.Label(
            self.frameInicial, text=self.descricoes["Porta"])
        self.widgets["labels"]["Porta"] = tk.Label(
            self.frameInicial, text=self.descricoes["Porta"])
        self.widgets["labels"]["HostLocal"] = tk.Label(
            self.frameInicial, text=self.hostLocalMensagem)
        self.widgets["labels"]["GIF"] = tk.Label(
            self.frameInicial, image=self.frames[0])
        self.widgets["labels"]["Conectando"] = tk.Label(
            self.frameInicial, text=self.descricoes["Conectando"])
        self.widgets["labels"]["PortaLocal"] = tk.Label(
            self.frameInicial, text=self.portaLocalMensagem)

        self.widgets["entries"]["Host"] = tk.Entry(self.frameInicial)
        self.widgets["entries"]["Porta"] = tk.Entry(self.frameInicial)
        self.widgets["buttons"]["Conectar"] = tk.Button(
            self.frameInicial, text="Conectar", command=self.exibir_caixa_mensagem_inicial)
        self.widgets["buttons"]["Cancelar"] = tk.Button(
            self.frameInicial, text="Cancelar", command=self.botao_cancelar_inicial)

    def grid_caixa_inicial(self):
        # Posicionar widgets usando o método grid
        self.widgets["labels"]["Host"].grid(row=2, column=0, padx=5, pady=5)
        self.widgets["labels"]["Porta"].grid(row=3, column=0, padx=5, pady=5)
        self.widgets["labels"]["HostLocal"].grid(
            row=0, column=0, columnspan=3, padx=0, pady=5)
        self.widgets["labels"]["PortaLocal"].grid(
            row=1, column=0, columnspan=3, padx=0, pady=5)
        self.widgets["entries"]["Host"].grid(
            row=2, column=1, padx=5, pady=5, columnspan=2)
        self.widgets["entries"]["Porta"].grid(
            row=3, column=1, padx=5, pady=5, columnspan=2)
        self.widgets["buttons"]["Conectar"].grid(
            row=5, column=1, padx=5, pady=5)
        self.widgets["buttons"]["Cancelar"].grid(
            row=5, column=2, padx=5, pady=5)
        self.widgets["buttons"]["Cancelar"].config(state='disabled')

    def botao_cancelar_inicial(self):
        # Desabilitar e esconder elementos após cancelar
        self.widgets["entries"]["Host"].config(state='normal')
        self.widgets["entries"]["Porta"].config(state='normal')
        self.widgets["buttons"]["Conectar"].config(state='normal')
        self.widgets["buttons"]["Cancelar"].config(state='disabled')
        self.widgets["labels"]["GIF"].grid_remove()
        self.widgets["labels"]["Conectando"].grid_remove()
        self.parada_thread = True
        self.thread_animacao.join()
        self.chatClienteSevidor.fecharConexao()
        try:
            self.chatClienteSevidor.flagThreadInicial.clear()
            self.chatClienteSevidor.flagThreadCliente.clear()
            self.chatClienteSevidor.flagThreadServidor.clear()
        except:
            pass

    # Métodos para animação e processamento de dados

    def atualizar_gif(self, ind):
        # Função para atualizar o GIF animado
        if self.parada_thread == True:
            return 0
        frame = self.frames[ind]
        ind += 1
        if ind == self.frameCnt:
            ind = 1
        self.widgets["labels"]["GIF"].configure(image=frame)
        self.frameInicial.after(100, self.atualizar_gif, ind)

    def executarGif(self):
        # Iniciar a animação do GIF
        self.widgets["labels"]["GIF"].grid(
            row=6, column=0, padx=10, pady=10, columnspan=4)
        self.widgets["labels"]["Conectando"].grid(
            row=7, column=0, padx=10, pady=10, columnspan=4)

        self.parada_thread = False
        self.thread_animacao = threading.Thread(
            target=self.atualizar_gif, args=(0,))
        self.thread_animacao.start()

    def exibir_caixa_mensagem_inicial(self):
        # Obter os valores das caixas de entrada
        self.host_porta = {
            "Host": self.widgets["entries"]["Host"].get(),
            "Porta": self.widgets["entries"]["Porta"].get()
        }

        if self.host_porta["Host"] and self.host_porta["Porta"]:
            self.widgets["buttons"]["Cancelar"].config(state='normal')

            mensagembox = f" {self.descricoes['Host']} {self.host_porta['Host']} \n {self.descricoes['Porta']} {self.host_porta['Porta']} "
            messagebox.showinfo("Caixa de Mensagem", mensagembox)
            self.widgets["entries"]["Host"].config(state='disabled')
            self.widgets["entries"]["Porta"].config(state='disabled')
            self.widgets["buttons"]["Conectar"].config(state='disabled')
            self.executarGif()
            self.conexaoDeUsuario()

        else:
            messagebox.showwarning("Caixa de Mensagem",
                                   "Por favor, digite um Host e uma Porta")

    def porta_disponivel(self, porta):
        # Verificar se a porta está disponível
        try:
            socket_temporario = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            socket_temporario.bind(("localhost", porta))
            socket_temporario.close()
            return True
        except socket.error:
            return False

    def encontrar_portas_disponiveis(self, porta_inicial, porta_final):
        # Encontrar uma porta disponível dentro do intervalo especificado
        for porta in range(porta_inicial, porta_final + 1):
            if self.porta_disponivel(porta):
                porta_disponivel = porta
                break
        return porta_disponivel

    def descobri_local_ip(self):
        # Obter o endereço IP local
        try:
            host_name = socket.gethostname()
            local_ip = socket.gethostbyname(host_name)
            return local_ip
        except socket.error as e:
            print(f"Não foi possível obter o endereço IP: {e}")
            return None

    def desligar(self):
        try:
            self.chatClienteSevidor.fecharConexao()
            self.chatClienteSevidor.flagThreadServidor.clear()
            self.chatClienteSevidor.flagThreadInicial.clear()
            self.chatClienteSevidor.flagThreadCliente.clear()
            # self.chatClienteSevidor.servidor.close()
        except:
            pass

        self.gerenteTelas.clear()
        self.destroy()

    def conexaoDeUsuario(self):
        print(self.hostLocal, self.portaLocal,
              self.host_porta['Host'], self.host_porta['Porta'])
        self.criar_chat()

        self.chatClienteSevidor = ChatClienteServidor(str(self.host_porta['Host']), int(
            self.host_porta['Porta']), str(self.hostLocal), int(self.portaLocal))
        
        self.thred_receber_mensagem = threading.Thread(
            target=self.receber_mensagem)
        self.thred_receber_mensagem.start()

        self.chatClienteSevidor.iniciar()
    

    def iniciar_tela_jogo(self):
        self.tela=tk.Frame(self)
        self.jogo=Jogo(self.tela)
    
    def estadosDeTelas(self):
        while True:
            if not self.gerenteTelas.is_set():
                break

            time.sleep(1)
            try:
                if self.chatClienteSevidor.flagThreadServidor.is_set():
                    self.frameInicial.grid_forget()
                self.iniciar_tela_jogo()
                self.frame_chat.grid(row=0, column=1, sticky='nsew')
                self.tela.grid(row=0, column=0, sticky='nsew')
            except:
                pass


    def criar_chat(self):
        self.frame_chat = tk.Frame(self,)
        
        self.exibicao_chat = scrolledtext.ScrolledText(
            self.frame_chat, state='disabled',width= 10,height= 30)
        self.exibicao_chat.grid(row=0, column=0, columnspan=3, sticky='nsew')

        self.caixa_entrada = tk.Entry(self.frame_chat)
        self.caixa_entrada.grid(row=1, column=0, sticky='ew')

        self.botao_enviar = tk.Button(
            self.frame_chat, text='Enviar', command=lambda: self.enviar_mensagem())
        self.botao_enviar.grid(row=1, column=1, sticky='e')

        self.mensagens = []

    def enviar_mensagem(self):
        usuario="Você"
        mensagemEnvio = self.caixa_entrada.get()
        self.estutura_mensagems["Mensagem"] = mensagemEnvio
        mensagem_json = json.dumps(self.estutura_mensagems)
        # mensagem_json = mensagem_json.encode('utf-8')

        self.chatClienteSevidor.flagThreadCliente.set()
        self.chatClienteSevidor.set_cliente(mensagem_json)
        self.mensagens.append(f"{usuario}: {mensagemEnvio}")
        self.atualizar_exibicao_chat()
        self.caixa_entrada.delete(0, 'end')
        thread_cliente = threading.Thread(target=self.chatClienteSevidor.enviar_mensagens)
        thread_cliente.start()

    def receber_mensagem(self):
        while True:
            if self.chatClienteSevidor.flagThreadServidor.is_set():
                break
            while True:
                time.sleep(1)
                self.atualizar_exibicao_chat()
                try:
                    if self.chatClienteSevidor.flagThreadServidor.is_set():
                        dados = self.chatClienteSevidor.socket_cliente.recv(1024)
                        if not dados:
                            break
                        # dados=dados.decode('utf-8')
                        print(dados)
                        mensagem_dicionario=json.loads(dados)
                        mensagem_dicionario_valor=mensagem_dicionario["Mensagem"]
                        self.mensagens.append(f"Oponente: {mensagem_dicionario_valor}")
                        self.atualizar_exibicao_chat()
                except Exception as e:
                    print(f"Erro na conexão: {e}")
                    break
            self.chatClienteSevidor.socket_cliente.close()

    def atualizar_exibicao_chat(self):
        try:
            self.exibicao_chat.config(state='normal')
            self.exibicao_chat.delete('1.0', END)
            for mensagem in self.mensagens:
                self.exibicao_chat.insert(END, mensagem + '\n')
            self.exibicao_chat.config(state='disabled')
            self.exibicao_chat.see(END)
        except:
            pass


####################################################################################################################################################################################
####################################################################################################################################################################################
class Jogo:
     def __init__(self,tela):
         self.tela = tela

         camada1=tk.Frame(self.tela,width=10,height=10,background="white")
         camada2=tk.Frame(self.tela,width=10,height=10,background="yellow")
         camada3=tk.Frame(self.tela,width=10,height=10,background="green")
         camada1.grid(row=0, column=0)
         camada2.grid(row=0, column=1)
         camada3.grid(row=0, column=2)
         None
    



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

def main():
    app = MeuAplicativoUI()
    app.mainloop()
    None


if __name__ == "__main__":
    # Iniciar o aplicativo
    main()
