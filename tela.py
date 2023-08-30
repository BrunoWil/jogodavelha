import tkinter as tk
from PIL import Image, ImageTk

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
        self.imagem_botao = Image.open("X.png")
        self.imagem_botao = self.imagem_botao.resize((50, 50))
        
        self.imagens_botoes = []  # Lista para armazenar as imagens individuais dos botões

        self.criar_camada("white", 0, "Camada 1")
        self.criar_camada("yellow", 1, "Camada 2")
        self.criar_camada("green", 2, "Camada 3")

    def criar_camada(self, cor, coluna, nome_camada):
        camada = tk.Frame(self.tela, width=100, height=150, background=cor)
        camada.grid(row=1, column=coluna, padx=10, pady=10)
        self.criar_matriz_botoes(camada)
        
        nomecamada = tk.Label(self.tela, text=nome_camada)
        nomecamada.grid(row=0, column=coluna, ipadx=5, ipady=5)

    def botao_clicado(self, botao, imagem):
        botao.config(image=imagem)
        botao.grid(ipadx=20,ipady=20,padx=2, pady=2)
        
    def criar_matriz_botoes(self, parent):
        for i in range(3):
            for j in range(3):
                botao = tk.Button(parent, text=f"Botão {i+1}-{j+1}")
                botao.grid(row=i, column=j, padx=2, pady=2, ipadx=20,ipady=20)
                
                # Crie uma nova instância da imagem para cada botão
                photo = ImageTk.PhotoImage(self.imagem_botao)
                self.imagens_botoes.append(photo)

                botao.config(command=lambda b=botao, p=photo: self.botao_clicado(b, p))

def main():
    app = MeuAplicativoUI()
    app.mainloop()

if __name__ == "__main__":
    main()
