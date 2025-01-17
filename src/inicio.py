import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database import Database  # Importa a classe Database

class JanelaPrincipal:
    def __init__(self):
        # Configurações gerais do CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configuração da janela principal
        self.root = ctk.CTk()
        self.root.title("Sistema de Controle de Funcionários")
        self.root.geometry("800x600")  # Tamanho da janela
        self.root.configure(fg_color='black')  # Cor de fundo da janela

        # Título
        ctk.CTkLabel(self.root, text="Bem Vindo", font=("Roboto", 24, "bold"), fg_color="transparent").pack(pady=(10, 0))

        # Frame esquerdo para os botões
        self.frame_botoes = ctk.CTkFrame(self.root, fg_color='black', border_color='darkgrey', border_width=1)
        self.frame_botoes.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        # Subtítulo
        ctk.CTkLabel(self.frame_botoes, text="Menu", font=("Roboto", 16, "bold"), fg_color="transparent").pack(pady=(10, 0))

        # Adicionando botões ao frame esquerdo
        self.criar_botoes()

        # Frame direito para a lista de aniversariantes
        self.frame_aniversariantes = ctk.CTkFrame(self.root, fg_color='black', border_color='darkgrey', border_width=1)
        self.frame_aniversariantes.pack(side="right", fill="both", expand=True, padx=20, pady=10)

        # Inicializa o banco de dados
        self.db = Database()  # Cria uma instância da classe Database
        
        # Adicionando a lista de aniversariantes
        self.criar_lista_aniversariantes()

        self.root.mainloop()

    def criar_botoes(self):
        botoes = [
            "Cadastro de Funcionários",
            "Registro de Ocorrências",
            "Registro de Férias",
            "Registro de Afastamentos",
            "Registro de Desligamentos",
            "Capacitação e Competências",
            "Medidas Disciplinares",
            "Configurações",
            "Ajuda",
            "Sair"
        ]

        for texto in botoes:
            botao = ctk.CTkButton(self.frame_botoes, text=texto, command=lambda t=texto: self.acao_botao(t))
            botao.pack(pady=10, padx=40, fill="x")

    def acao_botao(self, texto):
        messagebox.showinfo("Ação do Botão", f"Você clicou em: {texto}")

    def criar_lista_aniversariantes(self):
        # Título da lista
        ctk.CTkLabel(self.frame_aniversariantes, text="Aniversariantes do Mês", font=("Roboto", 16, "bold")).pack(pady=10)

        # Obtém a data atual
        hoje = datetime.now()
        dia_atual = hoje.day
        mes_atual = hoje.month

        # Busca todos os funcionários
        funcionarios = self.db.buscar_todos()
        #print(f"Funcionários------------------------------------: {funcionarios}")
        
        # Filtra os aniversariantes do mês
        for funcionario in funcionarios:
            nome = funcionario[1]
            data_nascimento = funcionario[9]  # Verifique se esta é a posição correta para a data de nascimento
            
            # Verifica se a data de nascimento não está vazia
            if data_nascimento:
                try:
                    # Converte a data de nascimento para o formato correto
                    ano_nascimento, mes_nascimento, dia_nascimento = map(int, data_nascimento.split('-'))
                    
                    # Verifica se o mês é igual e se o dia é igual
                    if mes_nascimento == mes_atual:
                        # Formata a data de aniversário para DD/MM
                        data_formatada = f"{dia_nascimento:02}/{mes_nascimento:02}"
                        emoji = "_  🎉 🎂  Parabéns!!!" if dia_nascimento == dia_atual else ""
                        ctk.CTkLabel(self.frame_aniversariantes, text=f"{nome}  _  {data_formatada}   {emoji}", fg_color="transparent").pack(anchor="w", padx=10)
                except ValueError:
                    print(f"Data de nascimento inválida para {nome}: {data_nascimento}")

if __name__ == "__main__":
    JanelaPrincipal()
