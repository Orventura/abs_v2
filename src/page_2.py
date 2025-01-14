import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime

class RegistroOcorrencias:
    def __init__(self):
        # Configurações gerais do CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configuração da janela principal
        self.root = ctk.CTk()
        self.root.title("Registro de Ocorrências")
        self.root.geometry("450x520")  # Tamanho mais compacto
        
        # Frame principal com cor de fundo preta
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#000000")
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

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RegistroOcorrencias()
    app.run()
