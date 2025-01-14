import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime
import locale
from tkinter import messagebox

class JanelaOcorrencias(ctk.CTkToplevel):
    def __init__(self, parent, database):
        super().__init__(parent)
        
        # Configurações da janela
        self.title("Registro de Ocorrências")
        self.geometry("800x600")
        
        # Referência ao banco de dados
        self.db = database
        
        # Configurar locale para português
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        
        # Criar interface
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self, fg_color="black")
        self.frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Campos do formulário
        # Data
        frame_data = ctk.CTkFrame(self.frame_principal, fg_color="black")
        frame_data.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(frame_data, text="Data:").pack(side="left", padx=5)
        self.data_entry = DateEntry(
            frame_data,
            locale='pt_BR',
            date_pattern='dd/mm/yyyy'
        )
        self.data_entry.pack(side="left", padx=5)
        
        # Matrícula e busca
        frame_matricula = ctk.CTkFrame(self.frame_principal, fg_color="black")
        frame_matricula.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(frame_matricula, text="Matrícula:").pack(side="left", padx=5)
        self.matricula_entry = ctk.CTkEntry(frame_matricula)
        self.matricula_entry.pack(side="left", padx=5)
        ctk.CTkButton(
            frame_matricula,
            text="Buscar",
            command=self.buscar_funcionario
        ).pack(side="left", padx=5)
        
        # Campos preenchidos automaticamente
        self.colaborador_var = ctk.StringVar()
        self.area_var = ctk.StringVar()
        self.turno_var = ctk.StringVar()
        
        # Colaborador
        frame_colab = ctk.CTkFrame(self.frame_principal, fg_color="black")
        frame_colab.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(frame_colab, text="Colaborador:").pack(side="left", padx=5)
        ctk.CTkEntry(
            frame_colab,
            textvariable=self.colaborador_var,
            state="readonly"
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        # Área e Turno
        frame_area_turno = ctk.CTkFrame(self.frame_principal, fg_color="black")
        frame_area_turno.pack(fill="x", padx=5, pady=5)
        
        # Área
        frame_area = ctk.CTkFrame(frame_area_turno, fg_color="black")
        frame_area.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkLabel(frame_area, text="Área:").pack(side="left", padx=5)
        ctk.CTkEntry(
            frame_area,
            textvariable=self.area_var,
            state="readonly"
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        # Turno
        frame_turno = ctk.CTkFrame(frame_area_turno, fg_color="black")
        frame_turno.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkLabel(frame_turno, text="Turno:").pack(side="left", padx=5)
        ctk.CTkEntry(
            frame_turno,
            textvariable=self.turno_var,
            state="readonly"
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        # Tipo de Ausência
        frame_tipo_ausencia = ctk.CTkFrame(self.frame_principal, fg_color="black")
        frame_tipo_ausencia.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(frame_tipo_ausencia, text="Tipo de Ausência:").pack(side="left", padx=5)
        self.tipo_ausencia = ctk.CTkComboBox(
            frame_tipo_ausencia,
            values=["Falta", "Atraso", "Saída Antecipada"]
        )
        self.tipo_ausencia.pack(side="left", padx=5)
        
        # Observação
        frame_obs = ctk.CTkFrame(self.frame_principal, fg_color="black")
        frame_obs.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(frame_obs, text="Observação:").pack(anchor="w", padx=5)
        self.observacao = ctk.CTkTextbox(frame_obs, height=100)
        self.observacao.pack(fill="x", padx=5, pady=5)
        
        # Justificado
        frame_justificado = ctk.CTkFrame(self.frame_principal, fg_color="black")
        frame_justificado.pack(fill="x", padx=5, pady=5)
        self.justificado = ctk.CTkCheckBox(
            frame_justificado,
            text="Justificado"
        )
        self.justificado.pack(side="left", padx=5)
        
       
        # Botões
        frame_botoes = ctk.CTkFrame(self.frame_principal, fg_color="black")
        frame_botoes.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            command=self.salvar_ocorrencia
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            frame_botoes,
            text="Limpar",
            command=self.limpar_campos
        ).pack(side="left", padx=5)
        
    def buscar_funcionario(self):
        matricula = self.matricula_entry.get()
        if not matricula:
            messagebox.showerror("Erro", "Por favor, insira uma matrícula")
            return
            
        funcionario = self.db.buscar_dados_funcionario_para_ocorrencia(matricula)
        if funcionario:
            self.colaborador_var.set(funcionario[1])  # nome
            self.area_var.set(funcionario[2])         # area
            self.turno_var.set(funcionario[3])        # turno
        else:
            messagebox.showerror("Erro", "Funcionário não encontrado")
            self.limpar_campos()
            
    def salvar_ocorrencia(self):
        # Coletar dados
        dados = (
            self.data_entry.get_date().strftime('%Y-%m-%d'),
            self.area_var.get(),
            self.turno_var.get(),
            self.matricula_entry.get(),
            self.colaborador_var.get(),
            self.tipo_ausencia.get(),
            self.observacao.get("1.0", "end-1c"),
            "Sim" if self.justificado.get() else "Não",
        )
        
        try:
            self.db.inserir_ocorrencia(dados)
            messagebox.showinfo("Sucesso", "Ocorrência registrada com sucesso!")
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar ocorrência: {str(e)}")
            
    def limpar_campos(self):
        self.matricula_entry.delete(0, 'end')
        self.colaborador_var.set("")
        self.area_var.set("")
        self.turno_var.set("")
        self.tipo_ausencia.set("")
        self.observacao.delete("1.0", "end")
        self.justificado.deselect()
        self.data_entry.set_date(datetime.now()) 