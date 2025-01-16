import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

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

        # Lista de aniversariantes (exemplo)
        aniversariantes = [
            ("João Silva", "01/01"),
            ("Maria Oliveira", "15/01"),
            ("Carlos Pereira", "20/01"),
            ("Ana Souza", "25/01"),
            ("Pedro Santos", "30/01"),
        ]

        # Criar uma lista para exibir os aniversariantes
        for nome, data in aniversariantes:
            ctk.CTkLabel(self.frame_aniversariantes, text=f"{nome} - {data}", fg_color="transparent").pack(anchor="w", padx=10)

if __name__ == "__main__":
    JanelaPrincipal()
