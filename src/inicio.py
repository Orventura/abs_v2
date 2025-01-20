import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database import Database  # Certifique-se de que esta classe está corretamente implementada
from app import App  # Certifique-se de que esta classe está corretamente implementada
from page_2 import RegistroOcorrencias  # Certifique-se de que esta classe está corretamente implementada
from ferias import RegistroFerias  # Certifique-se de que esta classe está corretamente implementada
from configuracoes import Configuracoes  # Certifique-se de que esta classe está corretamente implementada
from relatorios import Relatorios  # Certifique-se de que esta classe está corretamente implementada
from registro_desligamento import RegistroDesligamento  # Certifique-se de que esta classe está corretamente implementada
class JanelaPrincipal:
    def __init__(self):
        # Configurações gerais do CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configuração da janela principal
        self.root = ctk.CTk()
        self.root.title("Sistema de Controle de Funcionários")
        self.root.geometry("800x600")
        self.root.configure(fg_color='black')

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
        self.db = Database()

        # Adicionando a lista de aniversariantes
        self.criar_lista_aniversariantes()

        self.root.mainloop()

    def criar_botoes(self):
        botoes = [
            "Cadastro de Funcionários",
            "Registro de Ocorrências",
            "Registro de Desligamentos",
            "Registro de Férias",
            "Capacitação e Competências",
            "Medidas Disciplinares",
            "Relatórios",
            "Configurações",
            "Sair"
        ]

        for texto in botoes:
            botao = ctk.CTkButton(self.frame_botoes, text=texto, command=lambda t=texto: self.acao_botao(t))
            botao.pack(pady=10, padx=40, fill="x")

    def acao_botao(self, texto):
        if texto == "Cadastro de Funcionários":
            self.abrir_janela_top_2(App, "Cadastro de Funcionários")
        elif texto == "Registro de Ocorrências":
            self.abrir_janela_top_2(RegistroOcorrencias, "Registro de Ocorrências")
        elif texto == "Registro de Férias":
            self.abrir_janela_top_2(RegistroFerias, "Registro de Férias")
        elif texto == "Registro de Desligamentos":
            self.abrir_janela_top_2(RegistroDesligamento, "Registro de Desligamentos")
        elif texto == "Configurações":
            self.abrir_janela_top_2(Configuracoes, "Configurações")
        elif texto == "Sair":
            self.root.quit()
        elif texto == "Relatórios":
            self.abrir_janela_top_2(Relatorios, "Relatórios")
        else:
            messagebox.showinfo("Em Desenvolvimento", "Aguarde a próxima versão do sistema")

    def abrir_janela_top_2(self, JanelaClasse, titulo):
        self.root.withdraw()

        # Instancia a classe e acessa sua janela principal
        janela_top_2 = JanelaClasse()
        janela_top_2.root.protocol("WM_DELETE_WINDOW", lambda: self.fechar_janela_top_2(janela_top_2.root))
        janela_top_2.root.mainloop()


    def fechar_janela_top_2(self, janela):
        janela.destroy()
        self.root.deiconify()
        self.root.mainloop()

        

    def criar_lista_aniversariantes(self):
        # Título da lista
        ctk.CTkLabel(self.frame_aniversariantes, text="Aniversariantes do Mês", font=("Roboto", 16, "bold")).pack(pady=10)

        # Obtém a data atual
        hoje = datetime.now()
        dia_atual = hoje.day
        mes_atual = hoje.month

        # Busca todos os funcionários
        funcionarios = self.db.buscar_todos()

        # Filtra os aniversariantes do mês
        for funcionario in funcionarios:
            nome = funcionario[1]
            data_nascimento = funcionario[9]  # Verifique se esta é a posição correta para a data de nascimento

            if data_nascimento:
                try:
                    ano_nascimento, mes_nascimento, dia_nascimento = map(int, data_nascimento.split('-'))
                    if mes_nascimento == mes_atual:
                        data_formatada = f"{dia_nascimento:02}/{mes_nascimento:02}"
                        emoji = "_  🎉 🎂  Parabéns!!!" if dia_nascimento == dia_atual else ""
                        ctk.CTkLabel(self.frame_aniversariantes, text=f"{nome}  _  {data_formatada}   {emoji}", fg_color="transparent").pack(anchor="w", padx=10)
                except ValueError:
                    print(f"Data de nascimento inválida para {nome}: {data_nascimento}")

if __name__ == "__main__":
    JanelaPrincipal()