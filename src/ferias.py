import customtkinter as ctk
from tkinter import messagebox
from database import Database
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import locale

class RegistroFerias:
    def __init__(self):
        self.db = Database()
        
        # Configurações da janela
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Registro de Férias")
        self.root.geometry("450x600")
        self.root.configure(fg_color='black')
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#000000", border_width=1, border_color="white")
        self.main_frame.pack(expand=True, fill="both", padx=15, pady=15)

        # Criar formulário
        self.criar_formulario()
        
        # Criar botões
        self.criar_botoes()
        
    def criar_formulario(self):
        # Matrícula e botão buscar
        ctk.CTkLabel(self.main_frame, text="Matrícula:", fg_color="transparent").pack(anchor="w", padx=10, pady=(10,0))
        
        matricula_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        matricula_frame.pack(fill="x", padx=10, pady=(0,10))
        
        self.matricula_entry = ctk.CTkEntry(matricula_frame, width=150)
        self.matricula_entry.pack(side="left")
        
        self.buscar_btn = ctk.CTkButton(matricula_frame, text="Buscar", width=80, 
                                       command=self.buscar_funcionario,
                                       fg_color="#1f538d", hover_color="#1a4572")
        self.buscar_btn.pack(side="left", padx=(10,0))

        # Nome
        ctk.CTkLabel(self.main_frame, text="Nome:", fg_color="transparent").pack(anchor="w", padx=10)
        self.nome_entry = ctk.CTkEntry(self.main_frame, state="disabled")
        self.nome_entry.pack(fill="x", padx=10, pady=(0,10))

        # Função
        ctk.CTkLabel(self.main_frame, text="Função:", fg_color="transparent").pack(anchor="w", padx=10)
        self.funcao_entry = ctk.CTkEntry(self.main_frame, state="disabled")
        self.funcao_entry.pack(fill="x", padx=10, pady=(0,10))

        # Frame para CC e Desc. CC
        cc_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cc_frame.pack(fill="x", padx=10, pady=(0,10))

        # CC (lado esquerdo)
        cc_left = ctk.CTkFrame(cc_frame, fg_color="transparent")
        cc_left.pack(side="left", fill="x", expand=True, padx=(0,5))
        
        ctk.CTkLabel(cc_left, text="CC:", fg_color="transparent").pack(anchor="w")
        self.cc_entry = ctk.CTkEntry(cc_left)
        self.cc_entry.pack(fill="x")

        # Desc. CC (lado direito)
        cc_right = ctk.CTkFrame(cc_frame, fg_color="transparent")
        cc_right.pack(side="left", fill="x", expand=True, padx=(5,0))
        
        ctk.CTkLabel(cc_right, text="Desc. CC:", fg_color="transparent").pack(anchor="w")
        self.desc_cc_entry = ctk.CTkEntry(cc_right)
        self.desc_cc_entry.pack(fill="x")

        # Data de Admissão
        ctk.CTkLabel(self.main_frame, text="Admissão:", fg_color="transparent").pack(anchor="w", padx=10)
        self.admissao_entry = ctk.CTkEntry(self.main_frame, width=120, state="disabled")

        self.admissao_entry.pack(anchor="w", padx=10, pady=(0,10))

        # Frame para Início e Retorno
        datas_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        datas_frame.pack(fill="x", padx=10, pady=(0,10))

        # Data de Início
        inicio_frame = ctk.CTkFrame(datas_frame, fg_color="transparent")
        inicio_frame.pack(side="left", fill="x", expand=True, padx=(0,5))
        
        ctk.CTkLabel(inicio_frame, text="Início:", fg_color="transparent").pack(anchor="w")
        self.inicio_entry = DateEntry(inicio_frame, width=12, background='#1f538d',
                                    foreground='white', borderwidth=0,
                                    date_pattern='dd/mm/yyyy')
        self.inicio_entry.pack(anchor="w")
        
        # Data de Retorno
        retorno_frame = ctk.CTkFrame(datas_frame, fg_color="transparent")
        retorno_frame.pack(side="left", fill="x", expand=True, padx=(5,0))
        
        ctk.CTkLabel(retorno_frame, text="Retorno:", fg_color="transparent").pack(anchor="w")
        self.retorno_entry = DateEntry(retorno_frame, width=12, background='#1f538d',
                                     foreground='white', borderwidth=0,
                                     date_pattern='dd/mm/yyyy')
        self.retorno_entry.pack(anchor="w")
        self.retorno_entry.bind("<<DateEntrySelected>>", self.calcular_dias_gozo)

        # Dias de Gozo
        ctk.CTkLabel(self.main_frame, text="Dias de Gozo:", fg_color="transparent").pack(anchor="w", padx=10)
        self.gozo_entry = ctk.CTkEntry(self.main_frame, state="disabled")
        self.gozo_entry.pack(fill="x", padx=10, pady=(0,10))

    def criar_botoes(self):
        botoes_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=10, pady=10)
        
        self.salvar_btn = ctk.CTkButton(botoes_frame, text="Salvar", 
                                       command=self.salvar_ferias,
                                       fg_color="#1f538d", hover_color="#1a4572")
        self.salvar_btn.pack(side="left", padx=5)
        
        self.limpar_btn = ctk.CTkButton(botoes_frame, text="Limpar",
                                       command=self.limpar_campos,
                                       fg_color="#1f538d", hover_color="#1a4572")
        self.limpar_btn.pack(side="left", padx=5)

    def buscar_funcionario(self):
        
        try:
            matricula = self.matricula_entry.get()
            
            if not matricula:
                messagebox.showerror("Erro", "Por favor, insira uma matrícula")
                return
            
            # Primeiro busca o funcionário na tabela principal
            funcionario = self.db.buscar_por_matricula(matricula)
            if not funcionario:
                messagebox.showerror("Erro", "Funcionário não encontrado")
                return
            
            # Preenche dados básicos do funcionário
            self.nome_entry.configure(state="normal")
            self.nome_entry.delete(0, "end")
            self.nome_entry.insert(0, funcionario[1])
            self.nome_entry.configure(state="disabled")
            
            self.funcao_entry.configure(state="normal")
            self.funcao_entry.delete(0, "end")
            self.funcao_entry.insert(0, funcionario[2])
            self.funcao_entry.configure(state="disabled")
            
            # Configura data de admissão
            data_admissao = datetime.strptime(funcionario[8], '%Y-%m-%d')
            self.admissao_entry.configure(state="normal")
            self.admissao_entry.insert(0, data_admissao.strftime('%d/%m/%Y'))
            self.admissao_entry.configure(state="disabled")
            
            # Agora busca as férias do funcionário
            ferias = self.db.buscar_ferias_funcionario(matricula)
            if ferias:
                # Preenche todos os campos com os dados das férias
                self.cc_entry.delete(0, "end")
                self.cc_entry.insert(0, ferias[0])  # CC é o segundo campo
                
                self.desc_cc_entry.delete(0, "end")
                self.desc_cc_entry.insert(0, ferias[1])  # DESC_CC é o terceiro campo
                
                # Data de início
                if ferias[2]:  # dt_inicio é o quarto campo
                    data_inicio = datetime.strptime(ferias[2], '%Y-%m-%d')
                    self.inicio_entry.set_date(data_inicio)
                
                # Data de retorno
                if ferias[3]:  # dt_retorno é o quinto campo
                    data_retorno = datetime.strptime(ferias[3], '%Y-%m-%d')
                    self.retorno_entry.set_date(data_retorno)
                
                # Dias de gozo
                self.gozo_entry.configure(state="normal")
                self.gozo_entry.delete(0, "end")
                self.gozo_entry.insert(0, str(ferias[4]))  # dias_gozo é o sexto campo
                self.gozo_entry.configure(state="disabled")
                
                messagebox.showinfo("Informação", "Férias existentes carregadas com sucesso!")
            else:
                # Limpa os campos de férias para novo registro
                self.cc_entry.delete(0, "end")
                self.desc_cc_entry.delete(0, "end")
                self.gozo_entry.configure(state="normal")
                self.gozo_entry.delete(0, "end")
                self.gozo_entry.configure(state="disabled")
                # Configura as datas para a data atual
                hoje = datetime.now()
                self.inicio_entry.set_date(hoje)
                self.retorno_entry.set_date(hoje)
                
                messagebox.showinfo("Informação", "Novo registro de férias será criado!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar funcionário: {str(e)}")

    def calcular_dias_gozo(self, event=None):
        try:
            data_inicio = self.inicio_entry.get_date()
            data_retorno = self.retorno_entry.get_date()
            
            # Calcula a diferença em dias
            diferenca = (data_retorno - data_inicio).days
            
            # Habilita o campo temporariamente para atualizar o valor
            self.gozo_entry.configure(state="normal")
            self.gozo_entry.delete(0, "end")
            self.gozo_entry.insert(0, str(diferenca))
            self.gozo_entry.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular dias de gozo: {str(e)}")

    def salvar_ferias(self):
        try:
            matricula = self.matricula_entry.get()
            if not matricula:
                messagebox.showerror("Erro", "Por favor, insira uma matrícula")
                return
            
            # Verifica se os campos CC e DESC CC estão preenchidos
            cc = self.cc_entry.get().strip().upper()
            desc_cc = self.desc_cc_entry.get().strip().upper()
            
            if not cc or not desc_cc:
                messagebox.showerror("Erro", "Os campos CC e Desc. CC são obrigatórios!")
                return
            
            # Habilita temporariamente o campo de gozo para pegar o valor
            self.gozo_entry.configure(state="normal")
            dias_gozo = self.gozo_entry.get()
            self.gozo_entry.configure(state="disabled")

            # Converte a string da data de admissão para objeto datetime
            data_admissao = datetime.strptime(self.admissao_entry.get(), '%d/%m/%Y')
            
            # Prepara os dados como uma tupla na ordem correta
            dados = (
                self.nome_entry.get().upper(),  # Nome
                self.funcao_entry.get().upper(),  # Função
                cc,  # CC
                desc_cc.upper(),  # DESC_CC
                data_admissao.strftime('%Y-%m-%d'),  # Data Admissão
                self.inicio_entry.get_date().strftime('%Y-%m-%d'),  # Data Início
                self.retorno_entry.get_date().strftime('%Y-%m-%d'),  # Data Retorno
                int(dias_gozo),  # Dias de Gozo
                matricula  # Matrícula para o WHERE
            )
            
            # Verifica se já existem férias para esta matrícula
            ferias_existentes = self.db.buscar_ferias_funcionario(matricula)
            
            if ferias_existentes:
                # Atualiza o registro existente
                self.db.atualizar_ferias(dados)
                messagebox.showinfo("Sucesso", "Férias atualizadas com sucesso!")
            else:
                # Para inserção, reorganiza os dados com matrícula primeiro
                dados_insercao = (
                    matricula.upper(),
                    self.nome_entry.get().upper(),
                    self.funcao_entry.get().upper(),
                    cc,
                    desc_cc,
                    data_admissao.strftime('%Y-%m-%d'),
                    self.inicio_entry.get_date().strftime('%Y-%m-%d'),
                    self.retorno_entry.get_date().strftime('%Y-%m-%d'),
                    int(dias_gozo)
                )
                # Insere novo registro
                self.db.inserir_ferias(dados_insercao)
                messagebox.showinfo("Sucesso", "Férias registradas com sucesso!")
            
            # Limpa os campos após salvar
            self.limpar_campos()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar férias: {str(e)}")

    def limpar_campos(self):
        self.matricula_entry.delete(0, "end")
        self.nome_entry.configure(state="normal")
        self.nome_entry.delete(0, "end")
        self.nome_entry.configure(state="disabled")
        self.funcao_entry.configure(state="normal")
        self.funcao_entry.delete(0, "end")
        self.funcao_entry.configure(state="disabled")
        self.cc_entry.delete(0, "end")
        self.desc_cc_entry.delete(0, "end")
        self.admissao_entry.configure(state="normal")
        self.admissao_entry.delete(0, "end")
        self.admissao_entry.configure(state="disabled")
        self.gozo_entry.configure(state="normal")
        self.gozo_entry.delete(0, "end")
        self.gozo_entry.configure(state="disabled")

if __name__ == "__main__":
    app = RegistroFerias()
    app.root.mainloop() 