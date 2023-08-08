import tkinter as tk
from tkinter import messagebox
import threading
import socket
from tkinter import StringVar

class MeuAplicativo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Meu Aplicativo")
        
        # Definir o tamanho da tela (largura x altura)
        self.geometry("220x280")

        # # Criar widgets
        self.criar_widgets()
        self.frame_caixa_inicial()
        self.grid_caixa_inicial()
        
        # Lista para armazenar os textos digitados nas caixas de texto
        self.texto = []

    def criar_widgets(self):
        # Criação de listas para armazenar os widgets criados dinamicamente
        self.mensagens = ["Host:", "Porta:","Conectando"]
        self.hostLocal = f"Host Local: {self.descobri_local_ip()}"
        self.portaLocal = f"Porta Local: {self.encontrar_portas_disponiveis(1058, 47808)}"
        self.host_porta = []
        self.labels = []
        self.entries = []
        self.buttons = []
        self.frameCnt = 12
        self.frames = [tk.PhotoImage(file='carregando.gif', format='gif -index %i' % i).subsample(50,50) for i in range(self.frameCnt)]    

        # Criação de rótulos, caixas de texto e botão

    def frame_caixa_inicial(self):
        self.labels.append(tk.Label(self, text=self.mensagens[0]))# Caixa de texto Host
        self.labels.append(tk.Label(self, text=self.mensagens[1]))# Caixa de texto Porta
        self.labels.append(tk.Label(self, text=self.hostLocal))# Caixa de texto Host
        self.labels.append(tk.Label(self, image = self.frames[0]))# Caixa de texto para digitar a mensagem Host
        self.labels.append(tk.Label(self, text=self.mensagens[2]))# Caixa de texto Conectando
        self.labels.append(tk.Label(self, text=self.portaLocal))# Caixa de texto Conectando

        self.entries.append(tk.Entry(self))  # Caixa de texto para digitar a mensagem Host
        self.entries.append(tk.Entry(self))  # Caixa de texto para digitar a mensagem Porta
        self.buttons.append(tk.Button(self, text="Conectar", command=self.exibir_caixa_mensagem_inicial))
        self.buttons.append(tk.Button(self, text="Cancelar", command=self.botao_cancelar_inicial))


        # Posicionamento dos widgets usando grid
    def grid_caixa_inicial(self):
        self.labels[0].grid(row=2, column=0, padx=5, pady=5)# Caixa de texto Host
        self.labels[1].grid(row=3, column=0, padx=5, pady=5)# Caixa de texto Porta

        self.labels[2].grid(row=0, column=0, columnspan=3, padx=0, pady=5)# Caixa de texto meuHost
        self.labels[5].grid(row=1, column=0, columnspan=3, padx=0, pady=5)# Caixa de texto minhaPorta

        self.entries[0].grid(row=2, column=1, padx=5, pady=5,columnspan=2)# Caixa de texto para digitar a mensagem Host
        self.entries[1].grid(row=3, column=1, padx=5, pady=5,columnspan=2)# Caixa de texto para digitar a mensagem Porta
        self.buttons[0].grid(row=5, column=1, padx=5, pady=5)# Botão de conectar
        self.buttons[1].grid(row=5, column=2, padx=5, pady=5)# Botão de Cancelar
        self.buttons[1].config(state='disabled')# Botão de Cancelar


    def botao_cancelar_inicial(self):
        self.entries[0].config(state='normal')
        self.entries[1].config(state='normal')
        self.buttons[0].config(state='normal')
        self.buttons[1].config(state='disabled')
        self.labels[3].grid_remove()
        self.labels[4].grid_remove()
        self.parada_thread = True
        self.thread_animacao.join()

    def descobri_local_ip(self):
        try:
            # Obtém o nome do host local
            host_name = socket.gethostname()
            
            # Obtém o endereço IP associado ao nome do host local
            local_ip = socket.gethostbyname(host_name)
            
            return local_ip

        except socket.error as e:
            print(f"Não foi possível obter o endereço IP: {e}")
            return None

    def atualizar_gif(self,ind):
        if self.parada_thread == True:
            return 0
        frame = self.frames[ind]
        ind += 1
        if ind == self.frameCnt:
            ind = 1
        self.labels[3].configure(image=frame)
        app.after(100, self.atualizar_gif, ind)

    def executarGif(self):
        self.labels[3].grid(row=6, column=0, padx=10, pady=10,columnspan=4)
        self.labels[4].grid(row=7, column=0, padx=10, pady=10,columnspan=4)
        
        self.parada_thread = False
        self.thread_animacao = threading.Thread(target=self.atualizar_gif, args=(0,))
        self.thread_animacao.start()

    def exibir_caixa_mensagem_inicial(self):
        # Obter os textos digitados nas caixas de texto
        if not self.host_porta:
            self.host_porta.append([self.entries[0].get(),self.entries[1].get()])
        else:
            self.host_porta[0] = [self.entries[0].get(),self.entries[1].get()]


        

        # Verificar se há mensagem digitada
        if self.host_porta[0][0] and self.host_porta[0][1]:
            self.buttons[1].config(state='normal')#Habilitar o botão Cancelar

            # Exibir a caixa de mensagem com o conteúdo das caixas de texto
            messagebox.showinfo("Caixa de Mensagem", f"{self.mensagens[0]} {self.host_porta[0][0]}\n{self.mensagens[1]} {self.host_porta[0][1]}")
            self.entries[0].config(state='disabled')
            self.entries[1].config(state='disabled')
            self.buttons[0].config(state='disabled')
            self.executarGif()
        else:
            # Exibir um aviso se não houver mensagem digitada
            messagebox.showwarning("Caixa de Mensagem", "Por favor, digite um Host e uma Porta")

    def porta_disponivel(self, porta):
        try:
            socket_temporario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_temporario.bind(("localhost", porta))
            socket_temporario.close()
            return True
        except socket.error:
            return False

    def encontrar_portas_disponiveis(self, porta_inicial, porta_final):
        for porta in range(porta_inicial, porta_final + 1):
            if self.porta_disponivel(porta):
                porta_disponivel = porta
                break
        return porta_disponivel

if __name__ == "__main__":
    app = MeuAplicativo()
    app.mainloop()

