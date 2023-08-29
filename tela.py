import tkinter as tk
from tkinter import * 

class MeuAplicativoUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Meu Aplicativo")
        self.geometry("400x400")
        self.iniciar_tela_jogo()
    
    def iniciar_tela_jogo(self):
        self.tela = tk.Frame(self)
        self.tela.grid(row=0, column=0)
        self.jogo = Jogo(self.tela)

class Jogo:
    def __init__(self, tela):
        self.tela = tela
        
        self.criar_camada("white", 0, "Camada 1")
        self.criar_camada("yellow", 1, "Camada 2")
        self.criar_camada("green", 2, "Camada 3")
        self.imagens = []
          # Armazenar os botões de cada camada
        self.botao_cancelar = None
        self.botao_cancelar = tk.Button(self.tela, text="Cancelar Mudanças", command=self.cancelar_mudancas, state="disabled")



    def criar_camada(self, cor, coluna, nome_camada):
        camada = tk.Frame(self.tela, width=100, height=150, background=cor)
        camada.grid(row=1, column=coluna, padx=10, pady=10)
        self.criar_matriz_botoes(camada)
        
        nomecamada = tk.Label(self.tela, text=nome_camada)
        nomecamada.grid(row=0, column=coluna, ipadx=5, ipady=5)

    def botao_clicado(self, botao, imagem):
        botao.config(image=imagem)
        botao.image = imagem
        self.botao_cancelar.config(state="normal")  # Habilitar o botão "Cancelar"
        
    def cancelar_mudancas(self):
        for botao in self.botoes_camadas:
            botao.config(image=None, text="Botão")
        self.botao_cancelar.config(state="disabled")  # Desabilitar o botão "Cancelar"
        
    def criar_botao_cancelar(self):

        self.botao_cancelar.grid(row=2, columnspan=3, pady=10)
        
    def criar_matriz_botoes(self, parent):
        self.botoes_camadas = []
        for i in range(3):
            for j in range(3):
                botao = tk.Button(parent, text=f"Botão {i+1}-{j+1}", width=10, height=5)
                botao.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                botao.config(command=lambda b=botao: self.botao_clicado(b, PhotoImage(file="X.png")))
                self.botoes_camadas.append(botao)

def main():
    app = MeuAplicativoUI()
    app.mainloop()

if __name__ == "__main__":
    main()
