import sys
import time
import tkinter as tk
from tkinter import messagebox
import threading
import socket
from tkinter import StringVar
from chatClienteServidor import ChatClienteServidor # Importar a classe ChatServidorCliente do arquivo chatClienteServidor.py
from tkinter import scrolledtext, END

class MeuAplicativo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Meu Aplicativo")
        
        # Definir o tamanho da tela (largura x altura)
        self.geometry("220x280")

        # Criar widgets

        # Criar um frame para os widgets iniciais
        self.frameInicial = tk.Frame(self, borderwidth=2, relief="groove")
        self.frameInicial.grid(row=0, column=0, padx=10, pady=10)

        # Chamar os métodos para criar e posicionar os widgets
        self.criar_widgets()
        self.grid_caixa_inicial()

        # Lista para armazenar os textos digitados nas caixas de texto
        self.texto = []
        
        # Dicionário para armazenar valores de host e porta
        self.host_porta = {"Porta", "Host"}
        self.criar_chat()
        


    def criar_widgets(self):
        # Definir mensagens padrão
        self.descricoes = {
            "Host": "Host:",
            "Porta": "Porta:",
            "Conectando": "Conectando"
        }

        # Obter informações de host local e porta local
        self.porta1=1060
        self.hostLocalMensagem = f"Host Local: {self.descobri_local_ip()}"
        self.portaLocalMensagem = f"Porta Local: {self.encontrar_portas_disponiveis(self.porta1, 47808)}"
        self.hostLocal = self.descobri_local_ip()
        self.portaLocal = self.encontrar_portas_disponiveis(self.porta1, 47808)
        
        # Criar dicionário para armazenar widgets
        self.widgets = {
            "labels": {},
            "entries": {},
            "buttons": {}
        }

        # Carregar frames para animação
        self.frameCnt = 12
        self.frames = [tk.PhotoImage(file='carregando.gif', format='gif -index %i' % i).subsample(50, 50) for i in range(self.frameCnt)]

        # Criar rótulos, caixas de texto e botão
        self.frame_caixa_inicial()

    def frame_caixa_inicial(self):
        # Criar e posicionar widgets usando o método grid
        self.widgets["labels"]["Host"] = tk.Label(self.frameInicial, text=self.descricoes["Host"])
        self.widgets["labels"]["Porta"] = tk.Label(self.frameInicial, text=self.descricoes["Porta"])
        self.widgets["labels"]["Porta"] = tk.Label(self.frameInicial, text=self.descricoes["Porta"])
        self.widgets["labels"]["HostLocal"] = tk.Label(self.frameInicial, text=self.hostLocalMensagem)
        self.widgets["labels"]["GIF"] = tk.Label(self.frameInicial, image=self.frames[0])
        self.widgets["labels"]["Conectando"] = tk.Label(self.frameInicial, text=self.descricoes["Conectando"])
        self.widgets["labels"]["PortaLocal"] = tk.Label(self.frameInicial, text=self.portaLocalMensagem)

        self.widgets["entries"]["Host"] = tk.Entry(self.frameInicial)
        self.widgets["entries"]["Porta"] = tk.Entry(self.frameInicial)
        self.widgets["buttons"]["Conectar"] = tk.Button(self.frameInicial, text="Conectar", command=self.exibir_caixa_mensagem_inicial)
        self.widgets["buttons"]["Cancelar"] = tk.Button(self.frameInicial, text="Cancelar", command=self.botao_cancelar_inicial)

    def grid_caixa_inicial(self):
        # Posicionar widgets usando o método grid
        self.widgets["labels"]["Host"].grid(row=2, column=0, padx=5, pady=5)
        self.widgets["labels"]["Porta"].grid(row=3, column=0, padx=5, pady=5)
        self.widgets["labels"]["HostLocal"].grid(row=0, column=0, columnspan=3, padx=0, pady=5)
        self.widgets["labels"]["PortaLocal"].grid(row=1, column=0, columnspan=3, padx=0, pady=5)
        self.widgets["entries"]["Host"].grid(row=2, column=1, padx=5, pady=5, columnspan=2)
        self.widgets["entries"]["Porta"].grid(row=3, column=1, padx=5, pady=5, columnspan=2)
        self.widgets["buttons"]["Conectar"].grid(row=5, column=1, padx=5, pady=5)
        self.widgets["buttons"]["Cancelar"].grid(row=5, column=2, padx=5, pady=5)
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
        self.chatClienteSevidor.desligar()

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
        self.widgets["labels"]["GIF"].grid(row=6, column=0, padx=10, pady=10, columnspan=4)
        self.widgets["labels"]["Conectando"].grid(row=7, column=0, padx=10, pady=10, columnspan=4)
        
        self.parada_thread = False
        self.thread_animacao = threading.Thread(target=self.atualizar_gif, args=(0,))
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
            messagebox.showwarning("Caixa de Mensagem", "Por favor, digite um Host e uma Porta")

    def porta_disponivel(self, porta):
        # Verificar se a porta está disponível
        try:
            socket_temporario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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





    def criar_chat(self):
        self.frame_chat = tk.Frame(self)
        self.frame_chat.grid(row=5, column=5, sticky='nsew')

        self.exibicao_chat = scrolledtext.ScrolledText(self.frame_chat, state='disabled')
        self.exibicao_chat.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.caixa_entrada = tk.Entry(self.frame_chat)
        self.caixa_entrada.grid(row=1, column=0, sticky='ew')

        self.botao_enviar = tk.Button(self.frame_chat, text='Enviar', command=lambda:self.enviar_mensagem())
        self.botao_enviar.grid(row=1, column=1, sticky='e')

        self.mensagens = []
        
        self.recebimento_thread = threading.Thread(target=self.receber_mensagem, args=("Cliente",))
        self.recebimento_thread.start()

    def enviar_mensagem(self,usuario="Você"):
        mensagemEnvio = self.caixa_entrada.get()
        self.chatClienteSevidor.set_servidor(mensagemEnvio)
        self.mensagens.append(f"{usuario}: {mensagemEnvio}")
        self.atualizar_exibicao_chat()
        self.caixa_entrada.delete(0, 'end')

    def receber_mensagem(self, usuario):
        while True:
            mensagemReceber = sys.stdout
            # if str(mensagemReceber) != str("<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>") :
            self.mensagens.append(f"{usuario}: {mensagemReceber}")
            self.atualizar_exibicao_chat()
            time.sleep(1)

    def atualizar_exibicao_chat(self):
        self.exibicao_chat.config(state='normal')
        self.exibicao_chat.delete('1.0', END)
        for mensagem in self.mensagens:
            self.exibicao_chat.insert(END, mensagem + '\n')
        self.exibicao_chat.config(state='disabled')
        self.exibicao_chat.see(END)


    def conexaoDeUsuario(self): 
        print(self.hostLocal,self.portaLocal,self.host_porta['Host'],self.host_porta['Porta'])
        self.chatClienteSevidor = ChatClienteServidor(str(self.host_porta['Host']), int(self.host_porta['Porta']),str(self.hostLocal), int(self.portaLocal))
        self.chatClienteSevidor.iniciar()






































if __name__ == "__main__":
    # Iniciar o aplicativo
    app = MeuAplicativo()
    app.mainloop()
