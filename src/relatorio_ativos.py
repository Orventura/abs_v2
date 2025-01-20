import customtkinter as ctk
from tkinter import ttk
from database import Database
import tkinter as tk

class RelatorioAtivos:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.db = Database()
        
        # Configurações da janela
        self.root = ctk.CTk()
        self.root.title("Relatório - Colaboradores Ativos")
        self.root.geometry("1200x600")
        self.root.configure(fg_color='black')
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="black", border_width=1, border_color="white")
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Frame para o Treeview
        self.tree_frame = ctk.CTkFrame(self.main_frame, fg_color="black")
        self.tree_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Criar e configurar o Treeview
        self.criar_treeview()
        
        # Carregar dados
        self.carregar_dados()
        
        # Botões
        self.criar_botoes()
        
    def criar_treeview(self):
        # Estilo para o Treeview
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       borderwidth=0)
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       relief="flat")
        style.map("Treeview.Heading",
                 background=[('active', '#14375e')])
        
        # Criar Treeview
        self.tree = ttk.Treeview(self.tree_frame, style="Treeview")
        
        # Definir colunas
        self.tree["columns"] = ("Matrícula", "Nome", "Cargo", "Setor", "Empresa", 
                               "Turno", "Área", "Líder", "Admissão")
        
        # Formatação das colunas
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("Matrícula", width=80, anchor="center")
        self.tree.column("Nome", width=200, anchor="w")
        self.tree.column("Cargo", width=150, anchor="w")
        self.tree.column("Setor", width=120, anchor="w")
        self.tree.column("Empresa", width=120, anchor="w")
        self.tree.column("Turno", width=100, anchor="w")
        self.tree.column("Área", width=120, anchor="w")
        self.tree.column("Líder", width=150, anchor="w")
        self.tree.column("Admissão", width=100, anchor="center")
        
        # Cabeçalhos
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, anchor="center")
        
        # Scrollbars
        self.scrolly = ttk.Scrollbar(self.tree_frame, orient="vertical", 
                                   command=self.tree.yview)
        self.scrollx = ttk.Scrollbar(self.tree_frame, orient="horizontal", 
                                   command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.scrolly.set, 
                          xscrollcommand=self.scrollx.set)
        
        # Posicionamento
        self.scrolly.pack(side="right", fill="y")
        self.scrollx.pack(side="bottom", fill="x")
        self.tree.pack(expand=True, fill="both")
        
    def carregar_dados(self):
        # Limpar dados existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Buscar funcionários ativos
        query = """
        SELECT mat, nome, cargo, setor, empresa, turno, area, lider, dt_admissao 
        FROM funcionarios 
        WHERE UPPER(observacoes) NOT IN ('AFASTADO', 'DESLIGADO', 'FÉRIAS', 'FERIAS')
        ORDER BY nome
        """
        self.db.cursor.execute(query)
        funcionarios = self.db.cursor.fetchall()
        
        # Inserir dados no Treeview
        for func in funcionarios:
            self.tree.insert("", "end", values=func)
            
    def criar_botoes(self):
        botoes_frame = ctk.CTkFrame(self.main_frame, fg_color="#000000")
        botoes_frame.pack(fill="x", padx=10, pady=10)
        
        # Botão Atualizar
        ctk.CTkButton(
            botoes_frame,
            text="Atualizar",
            command=self.carregar_dados,
            width=120,
            fg_color="#1f538d",
            hover_color="#14375e"
        ).pack(side="left", padx=5)
        
        # Botão Exportar (para futura implementação)
        ctk.CTkButton(
            botoes_frame,
            text="Exportar",
            command=self.exportar_dados,
            width=120,
            fg_color="#1f538d",
            hover_color="#14375e"
        ).pack(side="left", padx=5)
    
    def exportar_dados(self):
        # Implementação futura para exportar dados
        pass

if __name__ == "__main__":
    app = RelatorioAtivos()
    app.root.mainloop() 