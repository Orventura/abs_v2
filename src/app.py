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
            ],
            "Informações Operacionais": [
                ("Número Rota", "num_rota"),
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
            if titulo == "Dados Funcionais":
                # Primeira linha: Matrícula, Data Admissão e Data Nascimento
                frame_linha1 = ctk.CTkFrame(frame_secao)
                frame_linha1.pack(fill="x", padx=10, pady=5)
                
                # Matrícula
                frame_mat = ctk.CTkFrame(frame_linha1)
                frame_mat.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_mat, text="Matrícula").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['mat'] = ctk.CTkEntry(frame_mat)
                self.entradas['mat'].pack(fill="x", padx=5, pady=(0,5))
                
                # Data Admissão
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
                
                # Data Nascimento
                frame_dt_nasc = ctk.CTkFrame(frame_linha1)
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
                
                # Segunda linha: Nome
                frame_linha2 = ctk.CTkFrame(frame_secao)
                frame_linha2.pack(fill="x", padx=10, pady=5)
                
                frame_nome = ctk.CTkFrame(frame_linha2)
                frame_nome.pack(fill="x", padx=5)
                ctk.CTkLabel(frame_nome, text="Nome").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['nome'] = ctk.CTkEntry(frame_nome)
                self.entradas['nome'].pack(fill="x", padx=5, pady=(0,5))
                
                # Terceira linha: Setor, Empresa e Área
                frame_linha3 = ctk.CTkFrame(frame_secao)
                frame_linha3.pack(fill="x", padx=10, pady=5)
                
                # Setor
                frame_setor = ctk.CTkFrame(frame_linha3)
                frame_setor.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_setor, text="Setor").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['setor'] = ctk.CTkComboBox(
                    frame_setor,
                    values=["Recebimento", "Expedição"]
                )
                self.entradas['setor'].pack(fill="x", padx=5, pady=(0,5))
                
                # Quarta linha: CPF, Cargo e Turno
                frame_linha4 = ctk.CTkFrame(frame_secao)
                frame_linha4.pack(fill="x", padx=10, pady=5)
                
                # CPF
                frame_cpf = ctk.CTkFrame(frame_linha4)
                frame_cpf.pack(side="left", fill="x", expand=0.45, padx=5)
                ctk.CTkLabel(frame_cpf, text="CPF").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['cpf'] = ctk.CTkEntry(frame_cpf)
                self.entradas['cpf'].pack(fill="x", padx=5, pady=(0,5))
                
                # Cargo
                frame_cargo = ctk.CTkFrame(frame_linha4)
                frame_cargo.pack(side="left", fill="x", expand=0.45, padx=5)
                ctk.CTkLabel(frame_cargo, text="Cargo").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['cargo'] = ctk.CTkEntry(frame_cargo)
                self.entradas['cargo'].pack(fill="x", padx=5, pady=(0,5))
                
                # Turno
                frame_turno = ctk.CTkFrame(frame_linha4)
                frame_turno.pack(side="left", fill="x", expand=0.1, padx=5)
                ctk.CTkLabel(frame_turno, text="Turno").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['turno'] = ctk.CTkComboBox(
                    frame_turno,
                    values=["A", "B", "C", "ADM1", "ADM2"]
                )
                self.entradas['turno'].pack(fill="x", padx=5, pady=(0,5))
                
                # Quinta linha: Área, Empresa e Líder
                frame_linha5 = ctk.CTkFrame(frame_secao)
                frame_linha5.pack(fill="x", padx=10, pady=5)
                
                # Área
                frame_area = ctk.CTkFrame(frame_linha5)
                frame_area.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_area, text="Área").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['area'] = ctk.CTkComboBox(
                    frame_area,
                    values=["A1", "A2", "A3", "B1", "ADM"]
                )
                self.entradas['area'].pack(fill="x", padx=5, pady=(0,5))
                
                # Empresa
                frame_empresa = ctk.CTkFrame(frame_linha5)
                frame_empresa.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_empresa, text="Empresa").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['empresa'] = ctk.CTkComboBox(
                    frame_empresa,
                    values=["PHILCO", "BRIC", "HUNT", "FENIX"]
                )
                self.entradas['empresa'].pack(fill="x", padx=5, pady=(0,5))
                
                # Líder
                frame_lider = ctk.CTkFrame(frame_linha5)
                frame_lider.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_lider, text="Líder").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['lider'] = ctk.CTkEntry(frame_lider)
                self.entradas['lider'].pack(fill="x", padx=5, pady=(0,5))
            elif titulo == "Informações Operacionais":
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
