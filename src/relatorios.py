import customtkinter as ctk
from tkinter import messagebox

class Relatorios:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title("Relatórios")
        self.root.geometry("600x400")
        self.root.configure(bg="black")

        self.frame_principal = ctk.CTkFrame(self.root, fg_color="black", border_width=1, border_color="white")
        self.frame_principal.pack(fill='both', expand=True, padx=10, pady=10)

        self.frame_titulo = ctk.CTkFrame(self.frame_principal, fg_color="black", border_width=0, border_color="red")
        self.frame_titulo.pack(fill="both", expand="no", padx=1, pady=1)

        self.label_titulo = ctk.CTkLabel(self.frame_titulo, text="Selecione o tipo de relatório", font=("Roboto", 16, "bold"), fg_color="black", text_color="white")
        self.label_titulo.pack(fill="both", expand="no", padx=1, pady=1)

        self.criar_botoes()

    
    def criar_botoes(self):

        self.frame_botoes = ctk.CTkFrame(self.frame_principal, fg_color="black", border_width=0, border_color="red")
        self.frame_botoes.pack(fill="x", expand='yes', padx=50, pady=50)

        botoes = [
            "Colaboradores Ativos",
            "ColaboradoresAfastados",
            "Faltas e Atrasos",
            "Férias",
        ]

        for texto in botoes:
            botao = ctk.CTkButton(self.frame_botoes, text=texto, command=lambda t=texto: self.acao_botao(t))
            botao.pack(fill="x", expand=False, padx=100, pady=5)



    def acao_botao(self, texto):
        if texto == "a":
            pass
        else:
            messagebox.showinfo("Em Desenvolvimento", "Aguarde a próxima versão do sistema")


if __name__ == "__main__":
    relatorios = Relatorios()
    relatorios.root.mainloop()