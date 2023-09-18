import json
import threading
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
    def __init__(self, tela,chatClienteSevidor,estutura_mensagems):
        self.chatClienteSevidor=chatClienteSevidor
        self.estutura_mensagems=estutura_mensagems
        self.tela_I=tela
        self.tela =tk.Frame(self.tela_I)
        self.tela.grid(row=0,column=0)
        self.imagem_vazia = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
        self.botao_desistir = tk.Button(self.tela, text="Desistir", font="20")
        self.botao_desistir.config(command=self.jogador_desistiu)

        self.imagens_botoes = []  # Lista para armazenar as imagens individuais dos botões
        self.botoes = {}  # Dicionário para armazenar botões por posição
        self.matriz_jogo = []
        self.matriz_de_jogo=[[[0 for k in range(3)] for j in range(3)] for i in range(3)]

        self.imagens_disponiveis = {
            "X": Image.open("X.png").resize((50, 50)),
            "O": Image.open("O.png").resize((50, 50)),
            "Vazia": self.imagem_vazia.resize((50, 50))
        }
        self.imagem_vazia_tk = ImageTk.PhotoImage(self.imagem_vazia)  

        self.criar_camada("white", 0, "Camada 1")
        self.criar_camada("yellow", 1, "Camada 2")
        self.criar_camada("green", 2, "Camada 3")
        self.venceu=tk.Label(self.tela,text="Você Ganhou",font="50")
        self.derrota=tk.Label(self.tela,text="Você Perdeu",font="50")
        self.desistiu_do_jogo = tk.Label(self.tela, text="Desistiu",font="30")

    def criar_camada(self, cor, coluna, nome_camada):
        camada = tk.Frame(self.tela, width=100, height=150, background=cor)
        camada.grid(row=2, column=coluna, padx=10, pady=10)
        self.criar_matriz_botoes(camada, coluna)
        
        nomecamada = tk.Label(self.tela, text=nome_camada)
        nomecamada.grid(row=1, column=coluna, ipadx=5, ipady=5)

        self.botao_desistir.grid(row=3, column=0,columnspan=3, ipadx=20, ipady=20)

    def botao_clicado(self, botao, imagem,c, i, j):

  
        self.qualvez("Oponente")
        posicao=(c,i,j)
        self.botoes[(c,i,j)][1]=True
        self.enviar_jogada(posicao)
        
        print(posicao)
        photo = ImageTk.PhotoImage(imagem)
        botao.config(image=photo,state='disabled')
        botao.image = photo  
        botao.grid(ipadx=20, ipady=20, padx=2, pady=2)
        self.passado_para_proximo()

    def enviar_jogada(self,posicao,destino="Jogada"):
        estutura_mensagems={
        "Jogada":{},
        "Mensagem":{},
        "Estado_Vencedor":{},
        "Reinicio": {}
        }
        estutura_mensagems[destino] = posicao
        mensagem_json = json.dumps(estutura_mensagems)
        self.chatClienteSevidor.flagThreadCliente.set()
        self.chatClienteSevidor.set_cliente(mensagem_json)
        thread_cliente = threading.Thread(target=self.chatClienteSevidor.enviar_mensagens)
        thread_cliente.start()

    def passado_para_proximo(self):
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    if self.botoes[(a, b, c)][1]==False:
                        self.botoes[(a, b, c)][0].config(state='disabled')

    def passado_para_mim(self):
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    if self.botoes[(a, b, c)][1]==False:
                        self.botoes[(a, b, c)][0].config(state='normal')      

    def criar_matriz_botoes(self, parent, coluna):
        for i in range(3):
            for j in range(3):
                botao = tk.Button(parent, image=self.imagem_vazia_tk)  # Usar a imagem vazia com referência
                botao.grid(row=i, column=j, padx=2, pady=2, ipadx=20, ipady=20)
                clicado=False
                self.botoes[(coluna, i, j)] = [botao,clicado]

                botao.config(command=lambda b=botao,c=coluna, i=i, j=j: self.botao_clicado(b, self.imagens_disponiveis["X"],c, i, j))


    def atualizar_imagem_botao(self, posicao, imagem="O"):
        self.qualvez("Sua vez")
        self.passado_para_mim()
        print(type(posicao))
        c=int(posicao[0])
        i=int(posicao[1])
        j=int(posicao[2])
        botao = self.botoes[(c, i, j)][0]
        self.botoes[(c,i,j)][1]=True
        self.matriz_de_jogo[c][i][j]=1

        if botao:
            photo = ImageTk.PhotoImage(self.imagens_disponiveis[imagem])  
            botao.config(image=photo,state='disabled')
            botao.image = photo  
            botao.grid(ipadx=20, ipady=20, padx=2, pady=2)

        if self.verificar_vitoria():
            self.enviar_jogada(True,"Estado_Vencedor")
            print("Derrota")
            self.jogador_derrota()


    def qualvez(self,jogador):
        vez_de_jogo = tk.Label(self.tela, text=jogador)
        vez_de_jogo.grid(row=0, column=0,columnspan=3, ipadx=5, ipady=5)

    def jogador_desistiu(self):
        self.botao_desistir.grid_remove()

        self.desistiu_do_jogo.grid(row=3, column=0,columnspan=3, ipadx=20, ipady=20)
        self.enviar_jogada(True,"Estado_Vencedor")
        self.jogador_derrota()


    def verificar_vitoria(self,jogador=1):
        tabuleiro=self.matriz_de_jogo
        N=3
        # Verificar linhas
        for i in range(N):
            for j in range(N):
                soma = 0
                for k in range(N):
                    soma += tabuleiro[i][j][k]
                if soma == jogador * N:
                    return True
        
        # Verificar colunas
        for i in range(N):
            for k in range(N):
                soma = 0
                for j in range(N):
                    soma += tabuleiro[i][j][k]
                if soma == jogador * N:
                    return True
        
        # Verificar profundidades
        for j in range(N):
            for k in range(N):
                soma = 0
                for i in range(N):
                    soma += tabuleiro[i][j][k]
                if soma == jogador * N:
                    return True
        
        # Verificar diagonais principais
        for i in range(N):
            soma = 0
            for j in range(N):
                soma += tabuleiro[i][j][j]
            if soma == jogador * N:
                return True
        
        for i in range(N):
            soma = 0
            for k in range(N):
                soma += tabuleiro[i][k][k]
            if soma == jogador * N:
                return True
        
        for j in range(N):
            soma = 0
            for k in range(N):
                soma += tabuleiro[k][j][k]
            if soma == jogador * N:
                return True
        
        # Verificar diagonais secundárias
        for i in range(N):
            soma = 0
            for j in range(N):
                soma += tabuleiro[i][j][N-1-j]
            if soma == jogador * N:
                return True
        
        for i in range(N):
            soma = 0
            for k in range(N):
                soma += tabuleiro[i][N-1-k][k]
            if soma == jogador * N:
                return True
        
        for j in range(N):
            soma = 0
            for k in range(N):
                soma += tabuleiro[N-1-k][j][k]
            if soma == jogador * N:
                return True
            

        soma = 0
        soma = tabuleiro[0][0][0]+tabuleiro[1][1][1]+tabuleiro[2][2][2]
        if soma == jogador * N:
                return True
        
        soma = tabuleiro[0][2][0]+tabuleiro[1][1][1]+tabuleiro[2][0][2]
        if soma == jogador * N:
                return True
        
        soma = tabuleiro[0][2][2]+tabuleiro[1][1][1]+tabuleiro[2][0][0]
        if soma == jogador * N:
                return True
        
        soma = tabuleiro[0][0][2]+tabuleiro[1][1][1]+tabuleiro[2][2][0]
        if soma == jogador * N:
                return True
        
        # Se nenhuma das condições satisfeita, retornar False
        return False
    
    def verificar_vitoria_old(self, jogador=1):
        tabuleiro = self.matriz_de_jogo
        N = 3

        # Verificar linhas, colunas e profundidades
        for i in range(N):
            for j in range(N):
                linha_soma = sum(tabuleiro[i][j][k] for k in range(N))
                coluna_soma = sum(tabuleiro[i][k][j] for k in range(N))
                profundidade_soma = sum(tabuleiro[k][i][j] for k in range(N))

                if linha_soma == jogador * N or coluna_soma == jogador * N or profundidade_soma == jogador * N:
                    return True
        
        # Verificar diagonais principais e secundárias
        diagonal_principal_soma = sum(tabuleiro[i][i][i] for i in range(N))
        diagonal_secundaria_soma = sum(tabuleiro[i][i][N - 1 - i] for i in range(N))

        if diagonal_principal_soma == jogador * N or diagonal_secundaria_soma == jogador * N:
            return True

        # Se nenhuma das condições acima foi satisfeita, retornar False
        return False



    def jogador_venceu(self):

        self.venceu.grid(row=0, column=0,columnspan=4, rowspan=4, ipadx=5, ipady=5)
        self.passado_para_proximo()
        self.botao_desistir.grid_forget()

    def jogador_derrota(self):

        self.derrota.grid(row=0, column=0,columnspan=4, rowspan=4, ipadx=5, ipady=5)
        self.passado_para_proximo()
        self.botao_desistir.grid_forget()

    def reiniciar(self):
        for c in range(3):
            for i in range(3):
                for j in range(3):
                    botao=self.botoes[(c, i, j)][0]
                    self.botoes[(c, i, j)][1]=False
                    botao.config(image=self.imagem_vazia_tk, state='normal')
                    self.matriz_de_jogo[c][i][j] = 0
        try:
            self.venceu.grid_remove()
            self.derrota.grid_remove()
            self.desistiu_do_jogo.grid_remove()
            self.botao_desistir.grid(row=3, column=0,columnspan=3, ipadx=20, ipady=20)
        except:
            pass

        # self.passado_para_mim()
        # self.qualvez("Sua vez")

def main():
    app = MeuAplicativoUI()
    app.mainloop()

if __name__ == "__main__":
    main()
