import customtkinter as ctk
from tkinter import ttk
from database import Database
import tkinter as tk
import platform

class RelatorioAtivos:
    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.db = Database()
        
        # Configurações da janela
        self.root = ctk.CTk()
        self.root.title("Relatório - Colaboradores Ativos")
        
        # Identificar o sistema operacional e maximizar a janela
        sistema = platform.system().lower()
        if sistema == "windows":
            self.root.state('zoomed')
        elif sistema == "linux":
            self.root.attributes('-zoomed', True)
        elif sistema == "darwin":  # macOS
            self.root.attributes('-fullscreen', True)
        
        self.root.configure(fg_color='black')

        # Frame para o Titulo
        self.titulo_frame = ctk.CTkFrame(self.root, fg_color="black")
        self.titulo_frame.pack(expand=False, fill="both", padx=10, pady=10)

        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="black", border_width=1, border_color="white")
        self.main_frame.pack(expand="yes", fill="both", padx=10, pady=10)

        # Label para o Titulo
        self.titulo_label = ctk.CTkLabel(self.titulo_frame, text="Colaboradores Ativos", font=("Roboto", 16, "bold"))
        self.titulo_label.pack(pady=10)
        
        # Frame para o Treeview
        self.tree_frame = ctk.CTkFrame(self.main_frame, fg_color="black")
        self.tree_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Criar e configurar o Treeview
        self.criar_treeview()
        
        # Carregar dados
        self.carregar_dados()
        
        # Botões
        self.criar_botoes()

        self.info_total()
        
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
        self.tree["columns"] = ("Matrícula", "Nome", "PCD", "Cargo", "Setor", "Empresa", 
                               "Turno", "Área", "Líder", "Admissão", "Telefone", "Endereço", "Bairro", "Referência", "Rota", "Colete", "Sapato")
        
        # Formatação das colunas
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("Matrícula", width=80, anchor="center")
        self.tree.column("Nome", width=200, anchor="center")
        self.tree.column("PCD", width=150, anchor="center")
        self.tree.column("Cargo", width=150, anchor="center")
        self.tree.column("Setor", width=120, anchor="center")
        self.tree.column("Empresa", width=120, anchor="center")
        self.tree.column("Turno", width=100, anchor="center")
        self.tree.column("Área", width=120, anchor="center")
        self.tree.column("Líder", width=150, anchor="center")
        self.tree.column("Admissão", width=100, anchor="center")
        self.tree.column("Telefone", width=100, anchor="center")
        self.tree.column("Endereço", width=100, anchor="center")
        self.tree.column("Bairro", width=100, anchor="center")
        self.tree.column("Referência", width=100, anchor="center")
        self.tree.column("Rota", width=100, anchor="center")
        self.tree.column("Colete", width=100, anchor="center")
        self.tree.column("Sapato", width=100, anchor="center")
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
        SELECT mat, nome, pcd, cargo, setor, empresa, turno, area, lider, dt_admissao, telefone, endereco, bairro, referencia, num_rota, colete, sapato
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
        # Frame para os botões
        frame_botoes = ctk.CTkFrame(self.root, fg_color="#000000")
        frame_botoes.pack(fill="x", padx=10, pady=10)
        
        # Botão Atualizar
        ctk.CTkButton(
            frame_botoes,
            text="Atualizar",
            command=self.carregar_dados,
            width=120,
            fg_color="#1f538d",
            hover_color="#14375e"
        ).pack(side="left", padx=5)
        
        # Botão Exportar (para futura implementação)
        ctk.CTkButton(
            frame_botoes,
            text="Exportar",
            command=self.exportar_dados,
            width=120,
            fg_color="#1f538d",
            hover_color="#14375e"
        ).pack(side="left", padx=5)
    
    def exportar_dados(self):
        # Implementação futura para exportar dados
        pass

    def info_total(self):
        query = """
        SELECT COUNT(*) FROM funcionarios WHERE UPPER(observacoes) NOT IN ('AFASTADO', 'DESLIGADO', 'FÉRIAS', 'FERIAS')
        """
        self.db.cursor.execute(query)
        total = self.db.cursor.fetchone()[0]

        frame_info = ctk.CTkFrame(self.main_frame, fg_color="black")
        frame_info.pack(expand=False, fill="both", padx=10, pady=10)

        ctk.CTkLabel(frame_info, text=f"Total de Colaboradores Ativos: {total}", font=("Roboto", 12, "bold")).pack(pady=10)

if __name__ == "__main__":
    app = RelatorioAtivos()
    app.root.mainloop() 