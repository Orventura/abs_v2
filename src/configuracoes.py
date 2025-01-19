import customtkinter as ctk
from tkinter import messagebox
import os

class Configuracoes:
    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title("Configurações")
        self.root.geometry("600x700") 
        self.root.configure(fg_color='black')    # Ajustado para melhor visualização em duas colunas
        
        # Diretório para os arquivos de configuração
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Configurações das ComboBox
        self.configs = {
            'Setores': 'setores.txt',
            'Áreas': 'areas.txt',
            'Empresas': 'empresas.txt',
            'Turnos': 'turnos.txt',
            'Coletes': 'coletes.txt',
            'Observações': 'observacoes.txt',
            'Líderes': 'lideres.txt'
        }
        
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color='black')
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame para os widgets de configuração
        config_frame = ctk.CTkFrame(self.main_frame, fg_color='black')
        config_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Criar campos para cada configuração
        self.text_widgets = {}
        
        # Lista de configurações para dividir em duas colunas
        configs_list = list(self.configs.items())
        mid_point = len(configs_list) // 2
        
        # Frame para a coluna esquerda
        left_frame = ctk.CTkFrame(config_frame, fg_color='black', border_width=1, border_color='white')
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Frame para a coluna direita
        right_frame = ctk.CTkFrame(config_frame, fg_color='black', border_width=1, border_color='white')
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Criar widgets para a coluna esquerda
        for titulo, arquivo in configs_list[:mid_point]:
            self.criar_widget_configuracao(left_frame, titulo, arquivo)
        
        # Criar widgets para a coluna direita
        for titulo, arquivo in configs_list[mid_point:]:
            self.criar_widget_configuracao(right_frame, titulo, arquivo)
        
        # Frame para os botões
        button_frame = ctk.CTkFrame(self.main_frame, fg_color='black')
        button_frame.pack(fill="x", pady=10)
        
        # Botões centralizados
        ctk.CTkButton(
            button_frame,
            text="Salvar",
            command=self.salvar_todas_configuracoes,
            width=120
        ).pack(side="left", padx=5, expand=True)
           
    def criar_widget_configuracao(self, parent_frame, titulo, arquivo):
        # Frame para cada configuração
        frame = ctk.CTkFrame(parent_frame, fg_color='black')
        frame.pack(fill="x", padx=5, pady=5)
        
        # Título
        ctk.CTkLabel(
            frame,
            text=titulo,
            font=("Roboto", 14, "bold")
        ).pack(anchor="w", padx=5, pady=2)
        
        # Campo de texto
        text_widget = ctk.CTkTextbox(frame, height=100)
        text_widget.pack(fill="x", padx=5, pady=(0, 5))
        
        # Carregar conteúdo existente
        self.text_widgets[titulo] = text_widget
        self.carregar_configuracao(titulo, text_widget)
    
    def carregar_configuracao(self, config_name, text_widget):
        arquivo = os.path.join(self.config_dir, self.configs[config_name])
        try:
            if os.path.exists(arquivo):
                with open(arquivo, 'r', encoding='utf-8') as f:
                    text_widget.delete("1.0", "end")
                    text_widget.insert("1.0", f.read())
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar {config_name}: {str(e)}")
    
    def salvar_todas_configuracoes(self):
        try:
            for config_name, text_widget in self.text_widgets.items():
                arquivo = os.path.join(self.config_dir, self.configs[config_name])
                conteudo = text_widget.get("1.0", "end-1c")
                
                # Filtrar linhas vazias e espaços
                linhas = [linha.strip() for linha in conteudo.split('\n') if linha.strip()]
                
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(linhas))
            
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")

if __name__ == "__main__":
    app = Configuracoes()
    app.root.mainloop()