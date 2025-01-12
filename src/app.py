import customtkinter as ctk
from database import Database

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela principal
        self.title("Sistema de Cadastro de Funcionários")
        self.geometry("1000x600")
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Inicializa a conexão com o banco
        self.db = Database()
        
        # Criar os frames principais
        self.criar_frames()
        
        # Criar os elementos do formulário
        self.criar_formulario()
        
    def criar_frames(self):
        # Frame principal (agora fixo, não scrollable)
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame do formulário
        self.frame_form = ctk.CTkFrame(self.frame_principal)
        self.frame_form.pack(fill="both", expand=True, padx=10, pady=10)
        
    def criar_formulario(self):
        # Título
        self.label_titulo = ctk.CTkLabel(
            self.frame_form, 
            text="Cadastro de Funcionário",
            font=("Roboto", 20, "bold")
        )
        self.label_titulo.pack(pady=10)
        
        # Definição dos campos por seção
        campos = {
            "Dados Funcionais": [
                ("Matrícula", "mat"),
                ("Nome", "nome"),
                ("CPF", "cpf"),
                ("Data Nascimento", "dt_nascimento"),
                ("Data Admissão", "dt_admissao"),
                ("Cargo", "cargo"),
                ("Setor", "setor")
            ],
            "Informações Operacionais": [
                ("Empresa", "empresa"),
                ("Turno", "turno"),
                ("Área", "area"),
                ("Líder", "lider"),
                ("Número Rota", "num_rota"),
                ("Colete", "colete"),
                ("Sapato", "sapato")
            ],
            "Contato e Localização": [
                ("E-mail", "email"),
                ("Telefone", "telefone"),
                ("Telefone Recado", "tel_recado"),
                ("Endereço", "endereco"),
                ("Bairro", "bairro"),
                ("Referência", "referencia")
            ]
        }
        
        # Frame fixo para as três seções
        frame_secoes = ctk.CTkFrame(self.frame_form)
        frame_secoes.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Criar as três seções
        self.entradas = {}
        
        for titulo, campos_secao in campos.items():
            # Frame para cada seção
            frame_secao = ctk.CTkFrame(frame_secoes)
            frame_secao.pack(side="left", fill="both", expand=True, padx=5)
            
            # Título da seção
            label_secao = ctk.CTkLabel(
                frame_secao,
                text=titulo,
                font=("Roboto", 16, "bold")
            )
            label_secao.pack(pady=10)
            
            # Campos da seção
            for label_text, campo in campos_secao:
                frame = ctk.CTkFrame(frame_secao)
                frame.pack(fill="x", padx=10, pady=5)
                
                label = ctk.CTkLabel(frame, text=label_text)
                label.pack(anchor="w", padx=5, pady=(5,0))
                
                entrada = ctk.CTkEntry(frame)
                entrada.pack(fill="x", padx=5, pady=(0,5))
                
                self.entradas[campo] = entrada

if __name__ == "__main__":
    app = App()
    app.mainloop()
