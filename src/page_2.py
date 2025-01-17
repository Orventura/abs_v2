import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import messagebox
from database import Database

class RegistroOcorrencias:
    def __init__(self):
        # Inicializa o banco de dados
        self.db = Database()
        
        # Configurações gerais do CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configuração da janela principal
        self.root = ctk.CTk()
        self.root.title("Registro de Ocorrências")
        self.root.geometry("450x520")  # Tamanho mais compacto
        self.root.configure(bg='black')
        
        # Frame principal com cor de fundo preta
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#000000", border_width=1, border_color="white")
        self.main_frame.pack(expand=True, fill="both")

        # Data
        ctk.CTkLabel(self.main_frame, text="Data:", fg_color="transparent").pack(anchor="w", padx=10, pady=(10,0))
        self.data_entry = DateEntry(self.main_frame, width=12, background='#1f538d',
                                  foreground='white', borderwidth=0, date_pattern='dd/mm/yyyy')
        self.data_entry.pack(anchor="w", padx=10, pady=(0,10))

        # Matrícula e botão buscar
        ctk.CTkLabel(self.main_frame, text="Matrícula:", fg_color="transparent").pack(anchor="w", padx=10)
        
        # Frame para matrícula e botão buscar
        matricula_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        matricula_frame.pack(fill="x", padx=10, pady=(0,10))
        
        self.matricula_entry = ctk.CTkEntry(matricula_frame, width=150)
        self.matricula_entry.pack(side="left")
        
        self.buscar_btn = ctk.CTkButton(matricula_frame, text="Buscar", width=80, 
                                       fg_color="#1f538d", hover_color="#1a4572")
        self.buscar_btn.pack(side="left", padx=(10,0))

        # Colaborador
        ctk.CTkLabel(self.main_frame, text="Colaborador:", fg_color="transparent").pack(anchor="w", padx=10)
        self.colab_entry = ctk.CTkEntry(self.main_frame)
        self.colab_entry.pack(fill="x", padx=10, pady=(0,10))

        # Frame para Área e Turno
        area_turno_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        area_turno_frame.pack(fill="x", padx=10, pady=(0,10))

        # Área (lado esquerdo)
        area_frame = ctk.CTkFrame(area_turno_frame, fg_color="transparent")
        area_frame.pack(side="left", fill="x", expand=True, padx=(0,5))
        
        ctk.CTkLabel(area_frame, text="Área:", fg_color="transparent").pack(anchor="w")
        self.area_entry = ctk.CTkEntry(area_frame)
        self.area_entry.pack(fill="x")

        # Turno (lado direito)
        turno_frame = ctk.CTkFrame(area_turno_frame, fg_color="transparent")
        turno_frame.pack(side="left", fill="x", expand=True, padx=(5,0))
        
        ctk.CTkLabel(turno_frame, text="Turno:", fg_color="transparent").pack(anchor="w")
        self.turno_entry = ctk.CTkEntry(turno_frame)
        self.turno_entry.pack(fill="x")

        # Frame para Tipo de Ausência e Justificado
        ausencia_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ausencia_frame.pack(fill="x", padx=10, pady=(0,10))

        # Tipo de Ausência (lado esquerdo)
        ausencia_label_frame = ctk.CTkFrame(ausencia_frame, fg_color="transparent")
        ausencia_label_frame.pack(side="left")
        
        ctk.CTkLabel(ausencia_label_frame, text="Tipo de Ausência:", fg_color="transparent").pack(anchor="w")
        self.ausencia_combo = ctk.CTkOptionMenu(
            ausencia_label_frame,
            values=["Falta", "Atraso", "Saída Antecipada"],
            width=150
        )
        self.ausencia_combo.pack(anchor="w")
        self.ausencia_combo.set("Falta")

        # Justificado (lado direito)
        self.justificado_var = ctk.BooleanVar()
        self.justificado_check = ctk.CTkCheckBox(
            ausencia_frame,
            text="Justificado",
            variable=self.justificado_var,
            fg_color="#1f538d",
            hover_color="#1a4572"
        )
        self.justificado_check.pack(side="right", padx=(20,0), pady=(10,0))

        # Observação
        ctk.CTkLabel(self.main_frame, text="Observação:", fg_color="transparent").pack(anchor="w", padx=10)
        self.obs_text = ctk.CTkTextbox(self.main_frame, height=100)
        self.obs_text.pack(fill="x", padx=10, pady=(0,10))

        # Frame para botões
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        # Botões
        self.salvar_btn = ctk.CTkButton(self.btn_frame, text="Salvar", width=120,
                                       fg_color="#1f538d", hover_color="#1a4572")
        self.salvar_btn.pack(side="left", padx=5)

        self.limpar_btn = ctk.CTkButton(self.btn_frame, text="Limpar", width=120,
                                       fg_color="#1f538d", hover_color="#1a4572")
        self.limpar_btn.pack(side="left", padx=5)

        # Atualizar os botões com os comandos
        self.buscar_btn.configure(command=self.buscar_funcionario)
        self.salvar_btn.configure(command=self.salvar_ocorrencia)
        self.limpar_btn.configure(command=self.limpar_campos)

    def buscar_funcionario(self):
        matricula = self.matricula_entry.get()
        if not matricula:
            messagebox.showerror("Erro", "Por favor, insira uma matrícula")
            return
            
        funcionario = self.db.buscar_dados_funcionario_para_ocorrencia(matricula)
        if funcionario:
            self.colab_entry.delete(0, 'end')
            self.colab_entry.insert(0, funcionario[1])  # nome
            self.area_entry.delete(0, 'end')
            self.area_entry.insert(0, funcionario[2])   # area
            self.turno_entry.delete(0, 'end')
            self.turno_entry.insert(0, funcionario[3])  # turno
        else:
            messagebox.showerror("Erro", "Funcionário não encontrado")
            self.limpar_campos()

    def salvar_ocorrencia(self):
        # Validar campos obrigatórios
        if not all([
            self.matricula_entry.get(),
            self.colab_entry.get(),
            self.area_entry.get(),
            self.turno_entry.get()
        ]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")
            return

        # Coletar dados
        dados = (
            self.data_entry.get_date().strftime('%Y-%m-%d'),
            self.area_entry.get(),
            self.turno_entry.get(),
            self.matricula_entry.get(),
            self.colab_entry.get(),
            self.ausencia_combo.get(),
            self.obs_text.get("1.0", "end-1c"),
            "Sim" if self.justificado_var.get() else "Não"
        )
        
        try:
            self.db.inserir_ocorrencia(dados)
            messagebox.showinfo("Sucesso", "Ocorrência registrada com sucesso!")
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar ocorrência: {str(e)}")

    def limpar_campos(self):
        self.matricula_entry.delete(0, 'end')
        self.colab_entry.delete(0, 'end')
        self.area_entry.delete(0, 'end')
        self.turno_entry.delete(0, 'end')
        self.ausencia_combo.set("Falta")
        self.obs_text.delete("1.0", "end")
        self.justificado_var.set(False)
        self.data_entry.set_date(datetime.now())

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RegistroOcorrencias()
    app.run()
