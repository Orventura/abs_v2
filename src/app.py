import customtkinter as ctk
from database import Database
from tkcalendar import DateEntry
import locale

# Configurar locale para português
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela principal
        self.title("Sistema de Cadastro de Funcionários")
        self.geometry("1300x600")
        
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
                ("Cargo", "cargo")
                # Setor será ComboBox
            ],
            "Informações Operacionais": [
                # Turno será ComboBox
                ("Líder", "lider"),
                ("Número Rota", "num_rota"),
                ("Sapato", "sapato")
                # Empresa, Área e Colete são ComboBox
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
            if titulo == "Dados Funcionais":
                # Frame para matrícula e data de admissão
                frame_linha1 = ctk.CTkFrame(frame_secao)
                frame_linha1.pack(fill="x", padx=10, pady=5)
                
                # Frame para matrícula
                frame_mat = ctk.CTkFrame(frame_linha1)
                frame_mat.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_mat, text="Matrícula").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['mat'] = ctk.CTkEntry(frame_mat)
                self.entradas['mat'].pack(fill="x", padx=5, pady=(0,5))
                
                # Frame para data de admissão
                frame_dt_adm = ctk.CTkFrame(frame_linha1)
                frame_dt_adm.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_dt_adm, text="Data Admissão").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['dt_admissao'] = DateEntry(
                    frame_dt_adm,
                    locale='pt_BR',
                    date_pattern='dd/mm/yyyy',
                    background='darkblue',
                    foreground='white',
                    borderwidth=2
                )
                self.entradas['dt_admissao'].pack(fill="x", padx=5, pady=(0,5))
                
                # Frame para nome e data de nascimento
                frame_linha2 = ctk.CTkFrame(frame_secao)
                frame_linha2.pack(fill="x", padx=10, pady=5)
                
                # Frame para nome
                frame_nome = ctk.CTkFrame(frame_linha2)
                frame_nome.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_nome, text="Nome").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['nome'] = ctk.CTkEntry(frame_nome)
                self.entradas['nome'].pack(fill="x", padx=5, pady=(0,5))
                
                # Frame para data de nascimento
                frame_dt_nasc = ctk.CTkFrame(frame_linha2)
                frame_dt_nasc.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_dt_nasc, text="Data Nascimento").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['dt_nascimento'] = DateEntry(
                    frame_dt_nasc,
                    locale='pt_BR',
                    date_pattern='dd/mm/yyyy',
                    background='darkblue',
                    foreground='white',
                    borderwidth=2
                )
                self.entradas['dt_nascimento'].pack(fill="x", padx=5, pady=(0,5))
                
                # Adicionar Setor como ComboBox
                frame = ctk.CTkFrame(frame_secao)
                frame.pack(fill="x", padx=10, pady=5)
                ctk.CTkLabel(frame, text="Setor").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['setor'] = ctk.CTkComboBox(
                    frame,
                    values=["Recebimento", "Expedição"]
                )
                self.entradas['setor'].pack(fill="x", padx=5, pady=(0,5))
                
                # Continuar com os demais campos da seção
                for label_text, campo in campos_secao[2:]:  # Pular os campos já criados
                    frame = ctk.CTkFrame(frame_secao)
                    frame.pack(fill="x", padx=10, pady=5)
                    
                    label = ctk.CTkLabel(frame, text=label_text)
                    label.pack(anchor="w", padx=5, pady=(5,0))
                    
                    entrada = ctk.CTkEntry(frame)
                    entrada.pack(fill="x", padx=5, pady=(0,5))
                    
                    self.entradas[campo] = entrada
            elif titulo == "Informações Operacionais":
                # Empresa
                frame = ctk.CTkFrame(frame_secao)
                frame.pack(fill="x", padx=10, pady=5)
                ctk.CTkLabel(frame, text="Empresa").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['empresa'] = ctk.CTkComboBox(
                    frame,
                    values=["Philco", "Bric", "Hunt", "Fênix"]
                )
                self.entradas['empresa'].pack(fill="x", padx=5, pady=(0,5))

                # Área
                frame = ctk.CTkFrame(frame_secao)
                frame.pack(fill="x", padx=10, pady=5)
                ctk.CTkLabel(frame, text="Área").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['area'] = ctk.CTkComboBox(
                    frame,
                    values=["A1", "A2", "A3", "B1", "ADM"]
                )
                self.entradas['area'].pack(fill="x", padx=5, pady=(0,5))

                # Turno
                frame = ctk.CTkFrame(frame_secao)
                frame.pack(fill="x", padx=10, pady=5)
                ctk.CTkLabel(frame, text="Turno").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['turno'] = ctk.CTkComboBox(
                    frame,
                    values=["A", "B", "C", "ADM1", "ADM2"]
                )
                self.entradas['turno'].pack(fill="x", padx=5, pady=(0,5))

                # Colete
                frame = ctk.CTkFrame(frame_secao)
                frame.pack(fill="x", padx=10, pady=5)
                ctk.CTkLabel(frame, text="Colete").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['colete'] = ctk.CTkComboBox(
                    frame,
                    values=["PP", "P", "M", "G", "GG"]
                )
                self.entradas['colete'].pack(fill="x", padx=5, pady=(0,5))

                # Continuar com os demais campos da seção
                for label_text, campo in campos_secao:
                    frame = ctk.CTkFrame(frame_secao)
                    frame.pack(fill="x", padx=10, pady=5)
                    
                    label = ctk.CTkLabel(frame, text=label_text)
                    label.pack(anchor="w", padx=5, pady=(5,0))
                    
                    entrada = ctk.CTkEntry(frame)
                    entrada.pack(fill="x", padx=5, pady=(0,5))
                    
                    self.entradas[campo] = entrada
            else:  # Contato e Localização
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
