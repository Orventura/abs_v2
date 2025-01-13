import customtkinter as ctk
from database import Database
from tkcalendar import DateEntry
import locale
from datetime import datetime
from tkinter import messagebox
from components import Validacoes

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
            "Dados do Colaborador": [
                ("Matrícula", "mat"),
                ("Nome", "nome"),
                ("CPF", "cpf"),
                ("Cargo", "cargo")
            ],
            "Contatos e Outros": [
                ("Número Rota", "num_rota"),
                ("Sapato", "sapato"),
                ("E-mail", "email"),
                ("Telefone", "telefone"),
                ("Telefone Recado", "tel_recado"),
                ("Endereço", "endereco"),
                ("Bairro", "bairro"),
                ("Referência", "referencia")
            ]
        }
        
        # Frame fixo para as duas seções
        frame_secoes = ctk.CTkFrame(self.frame_form)
        frame_secoes.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Criar as duas seções
        self.entradas = {}
        
        for titulo, campos_secao in campos.items():
            # Frame para cada seção (ajustado para ocupar metade do espaço)
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
            if titulo == "Dados do Colaborador":
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
                
                # Terceira linha: Setor, Observação e PCD
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
                
                # Observação
                frame_obs = ctk.CTkFrame(frame_linha3)
                frame_obs.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_obs, text="Observação").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['observacao'] = ctk.CTkComboBox(
                    frame_obs,
                    values=["Afastado", "Ativo"]
                )
                self.entradas['observacao'].pack(fill="x", padx=5, pady=(0,5))
                
                # PCD
                frame_pcd = ctk.CTkFrame(frame_linha3)
                frame_pcd.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_pcd, text="PCD").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['pcd'] = ctk.CTkCheckBox(
                    frame_pcd,
                    text="",
                    onvalue=True,
                    offvalue=False
                )
                self.entradas['pcd'].pack(fill="x", padx=5, pady=(0,5))
                
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
            elif titulo == "Contatos e Outros":
                # Primeira linha: Colete, Sapato e Número da Rota
                frame_linha1 = ctk.CTkFrame(frame_secao)
                frame_linha1.pack(fill="x", padx=10, pady=5)
                
                # Colete
                frame_colete = ctk.CTkFrame(frame_linha1)
                frame_colete.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_colete, text="Colete").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['colete'] = ctk.CTkComboBox(
                    frame_colete,
                    values=["PP", "P", "M", "G", "GG"]
                )
                self.entradas['colete'].pack(fill="x", padx=5, pady=(0,5))
                
                # Sapato
                frame_sapato = ctk.CTkFrame(frame_linha1)
                frame_sapato.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_sapato, text="Sapato").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['sapato'] = ctk.CTkEntry(frame_sapato)
                self.entradas['sapato'].pack(fill="x", padx=5, pady=(0,5))
                
                # Número da Rota
                frame_rota = ctk.CTkFrame(frame_linha1)
                frame_rota.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_rota, text="Número Rota").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['num_rota'] = ctk.CTkEntry(frame_rota)
                self.entradas['num_rota'].pack(fill="x", padx=5, pady=(0,5))
                
                # Segunda linha: Email
                frame_linha2 = ctk.CTkFrame(frame_secao)
                frame_linha2.pack(fill="x", padx=10, pady=5)
                ctk.CTkLabel(frame_linha2, text="E-mail").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['email'] = ctk.CTkEntry(frame_linha2)
                self.entradas['email'].pack(fill="x", padx=5, pady=(0,5))
                
                # Terceira linha: Telefone e Telefone Recado
                frame_linha3 = ctk.CTkFrame(frame_secao)
                frame_linha3.pack(fill="x", padx=10, pady=5)
                
                # Telefone
                frame_tel = ctk.CTkFrame(frame_linha3)
                frame_tel.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_tel, text="Telefone").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['telefone'] = ctk.CTkEntry(frame_tel)
                self.entradas['telefone'].pack(fill="x", padx=5, pady=(0,5))
                
                # Telefone Recado
                frame_tel_rec = ctk.CTkFrame(frame_linha3)
                frame_tel_rec.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_tel_rec, text="Telefone Recado").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['tel_recado'] = ctk.CTkEntry(frame_tel_rec)
                self.entradas['tel_recado'].pack(fill="x", padx=5, pady=(0,5))
                
                # Quarta linha: Endereço e Bairro
                frame_linha4 = ctk.CTkFrame(frame_secao)
                frame_linha4.pack(fill="x", padx=10, pady=5)
                
                # Endereço
                frame_end = ctk.CTkFrame(frame_linha4)
                frame_end.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_end, text="Endereço").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['endereco'] = ctk.CTkEntry(frame_end)
                self.entradas['endereco'].pack(fill="x", padx=5, pady=(0,5))
                
                # Bairro
                frame_bairro = ctk.CTkFrame(frame_linha4)
                frame_bairro.pack(side="left", fill="x", expand=True, padx=5)
                ctk.CTkLabel(frame_bairro, text="Bairro").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['bairro'] = ctk.CTkEntry(frame_bairro)
                self.entradas['bairro'].pack(fill="x", padx=5, pady=(0,5))
                
                # Quinta linha: Referência
                frame_linha5 = ctk.CTkFrame(frame_secao)
                frame_linha5.pack(fill="x", padx=10, pady=5)
                ctk.CTkLabel(frame_linha5, text="Referência").pack(anchor="w", padx=5, pady=(5,0))
                self.entradas['referencia'] = ctk.CTkEntry(frame_linha5)
                self.entradas['referencia'].pack(fill="x", padx=5, pady=(0,5))

        # Frame para botões (após os frames de dados)
        self.frame_botoes = ctk.CTkFrame(self.frame_form)
        self.frame_botoes.pack(fill="x", padx=10, pady=10)
        
        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(
            self.frame_botoes,
            text="Salvar",
            command=self.salvar_funcionario,
            width=120
        )
        self.btn_salvar.pack(side="left", padx=5)
        
        # Botão Editar
        self.btn_editar = ctk.CTkButton(
            self.frame_botoes,
            text="Editar",
            command=self.editar_funcionario,
            width=120
        )
        self.btn_editar.pack(side="left", padx=5)

    def salvar_funcionario(self):
        # Cria um dicionário com os dados das entradas
        dados = {
            'mat': self.entradas['mat'].get(),
            'nome': self.entradas['nome'].get(),
            'cargo': self.entradas['cargo'].get(),
            'setor': self.entradas['setor'].get(),
            'empresa': self.entradas['empresa'].get(),
            'turno': self.entradas['turno'].get(),
            'area': self.entradas['area'].get(),
            'lider': self.entradas['lider'].get(),
            'dt_admissao': self.entradas['dt_admissao'].get_date().strftime('%Y-%m-%d'),
            'dt_nascimento': self.entradas['dt_nascimento'].get_date().strftime('%Y-%m-%d'),
            'cpf': self.entradas['cpf'].get(),
            'email': self.entradas['email'].get(),
            'endereco': self.entradas['endereco'].get(),
            'bairro': self.entradas['bairro'].get(),
            'referencia': self.entradas['referencia'].get(),
            'telefone': self.entradas['telefone'].get(),
            'tel_recado': self.entradas['tel_recado'].get(),
            'num_rota': self.entradas['num_rota'].get(),
            'colete': self.entradas['colete'].get(),
            'sapato': self.entradas['sapato'].get(),
            'pcd': "Sim" if self.entradas['pcd'].get() else "Não",
            'observacao': self.entradas['observacao'].get()
        }
        
        # Validar campos obrigatórios
        campos_vazios = Validacoes.validar_campos_obrigatorios(dados)
        if campos_vazios:
            self.mostrar_mensagem("Erro", f"Os seguintes campos são obrigatórios:\n{', '.join(campos_vazios)}")
            return
            
        # Validar CPF
        if not Validacoes.validar_cpf(dados['cpf']):
            self.mostrar_mensagem("Erro", "CPF inválido!")
            return
            
        # Validar email
        if not Validacoes.validar_email(dados['email']):
            self.mostrar_mensagem("Erro", "E-mail inválido!")
            return
            
        # Validar telefones
        if not Validacoes.validar_telefone(dados['telefone']):
            self.mostrar_mensagem("Erro", "Telefone inválido!")
            return
            
        if not Validacoes.validar_telefone(dados['tel_recado']):
            self.mostrar_mensagem("Erro", "Telefone para recado inválido!")
            return
        
        # Converter o dicionário em tupla na ordem correta para o banco
        dados_tupla = (
            dados['mat'], dados['nome'], dados['cargo'], dados['setor'],
            dados['empresa'], dados['turno'], dados['area'], dados['lider'],
            dados['dt_admissao'], dados['dt_nascimento'], dados['cpf'],
            dados['email'], dados['endereco'], dados['bairro'], dados['referencia'],
            dados['telefone'], dados['tel_recado'], dados['num_rota'],
            dados['colete'], dados['sapato'], dados['pcd'], dados['observacao']
        )
        
        try:
            # Verifica se já existe um funcionário com esta matrícula
            funcionario_existente = self.db.buscar_por_matricula(dados['mat'])
            
            if funcionario_existente:
                # Se existe, atualiza
                self.db.atualizar(dados_tupla)
                self.mostrar_mensagem("Sucesso", "Funcionário atualizado com sucesso!")
            else:
                # Se não existe, insere
                self.db.inserir(dados_tupla)
                self.mostrar_mensagem("Sucesso", "Funcionário cadastrado com sucesso!")
                
            # Limpa o formulário após salvar
            self.limpar_formulario()
            
        except Exception as e:
            self.mostrar_mensagem("Erro", f"Erro ao salvar funcionário: {str(e)}")
    
    def mostrar_mensagem(self, titulo, mensagem):
        """Exibe uma mensagem para o usuário"""
        if titulo == "Sucesso":
            messagebox.showinfo(titulo, mensagem)
        else:
            messagebox.showerror(titulo, mensagem)
    
    def limpar_formulario(self):
        """Limpa todos os campos do formulário"""
        for chave, entrada in self.entradas.items():
            if isinstance(entrada, ctk.CTkEntry):
                entrada.delete(0, 'end')
            elif isinstance(entrada, ctk.CTkComboBox):
                entrada.set('')  # Para ComboBox, usamos set ao invés de delete
            elif isinstance(entrada, ctk.CTkCheckBox):
                entrada.deselect()
            elif isinstance(entrada, DateEntry):
                entrada.set_date(datetime.now())

    def editar_funcionario(self):
        # Pegar a matrícula
        matricula = self.entradas['mat'].get()
        
        # Verificar se a matrícula foi preenchida
        if not matricula:
            self.mostrar_mensagem("Erro", "Por favor, insira a matrícula do funcionário para editar.")
            return
            
        # Buscar funcionário no banco
        funcionario = self.db.buscar_por_matricula(matricula)
        
        # Verificar se encontrou o funcionário
        if not funcionario:
            self.mostrar_mensagem("Erro", "Funcionário não encontrado com esta matrícula.")
            return
            
        try:
            # Preencher os campos com os dados do funcionário
            self.entradas['nome'].delete(0, 'end')
            self.entradas['nome'].insert(0, funcionario[1])
            
            self.entradas['cargo'].delete(0, 'end')
            self.entradas['cargo'].insert(0, funcionario[2])
            
            self.entradas['setor'].set(funcionario[3])
            self.entradas['empresa'].set(funcionario[4])
            self.entradas['turno'].set(funcionario[5])
            self.entradas['area'].set(funcionario[6])
            
            self.entradas['lider'].delete(0, 'end')
            self.entradas['lider'].insert(0, funcionario[7])
            
            # Converter string para data
            dt_admissao = datetime.strptime(funcionario[8], '%Y-%m-%d')
            dt_nascimento = datetime.strptime(funcionario[9], '%Y-%m-%d')
            
            self.entradas['dt_admissao'].set_date(dt_admissao)
            self.entradas['dt_nascimento'].set_date(dt_nascimento)
            
            self.entradas['cpf'].delete(0, 'end')
            self.entradas['cpf'].insert(0, funcionario[10])
            
            self.entradas['email'].delete(0, 'end')
            self.entradas['email'].insert(0, funcionario[11])
            
            self.entradas['endereco'].delete(0, 'end')
            self.entradas['endereco'].insert(0, funcionario[12])
            
            self.entradas['bairro'].delete(0, 'end')
            self.entradas['bairro'].insert(0, funcionario[13])
            
            self.entradas['referencia'].delete(0, 'end')
            self.entradas['referencia'].insert(0, funcionario[14])
            
            self.entradas['telefone'].delete(0, 'end')
            self.entradas['telefone'].insert(0, funcionario[15])
            
            self.entradas['tel_recado'].delete(0, 'end')
            self.entradas['tel_recado'].insert(0, funcionario[16])
            
            self.entradas['num_rota'].delete(0, 'end')
            self.entradas['num_rota'].insert(0, funcionario[17])
            
            self.entradas['colete'].set(funcionario[18])
            
            self.entradas['sapato'].delete(0, 'end')
            self.entradas['sapato'].insert(0, funcionario[19])
            
            # Configurar o checkbox PCD
            if funcionario[20] == "Sim":
                self.entradas['pcd'].select()
            else:
                self.entradas['pcd'].deselect()
                
            self.entradas['observacao'].set(funcionario[21])
            
            self.mostrar_mensagem("Sucesso", "Dados do funcionário carregados com sucesso!")
            
        except Exception as e:
            self.mostrar_mensagem("Erro", f"Erro ao carregar dados do funcionário: {str(e)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
