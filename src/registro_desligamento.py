import customtkinter as ctk
from tkinter import messagebox
from database import Database
from datetime import datetime
import os

class RegistroDesligamento:
    def __init__(self):
        self.db = Database()
        
        # Configurações da janela
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Registro de Desligamento")
        self.root.geometry("450x630")
        self.root.configure(fg_color='black')
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#000000", border_width=1, border_color="white")
        self.main_frame.pack(expand=True, fill="both", padx=15, pady=15)
        
        self.criar_formulario()
        self.carregar_opcoes_motivo()
        
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
        
        # Cargo
        ctk.CTkLabel(self.main_frame, text="Cargo:", fg_color="transparent").pack(anchor="w", padx=10)
        self.cargo_entry = ctk.CTkEntry(self.main_frame, state="disabled")
        self.cargo_entry.pack(fill="x", padx=10, pady=(0,10))
        
        # Setor
        ctk.CTkLabel(self.main_frame, text="Setor:", fg_color="transparent").pack(anchor="w", padx=10)
        self.setor_entry = ctk.CTkEntry(self.main_frame, state="disabled")
        self.setor_entry.pack(fill="x", padx=10, pady=(0,10))
        
        # Data de Admissão
        ctk.CTkLabel(self.main_frame, text="Data de Admissão:", fg_color="transparent").pack(anchor="w", padx=10)
        self.admissao_entry = ctk.CTkEntry(self.main_frame, state="disabled")
        self.admissao_entry.pack(fill="x", padx=10, pady=(0,10))
        
        # Motivo do Desligamento
        ctk.CTkLabel(self.main_frame, text="Motivo do Desligamento:", fg_color="transparent").pack(anchor="w", padx=10)
        self.motivo_combobox = ctk.CTkComboBox(self.main_frame, values=[""])
        self.motivo_combobox.pack(fill="x", padx=10, pady=(0,10))
        
        # Observação
        ctk.CTkLabel(self.main_frame, text="Observação:", fg_color="transparent").pack(anchor="w", padx=10)
        self.observacao_text = ctk.CTkTextbox(self.main_frame, height=100)
        self.observacao_text.pack(fill="x", padx=10, pady=(0,10))
        
        # Botões
        self.criar_botoes()
        
    def criar_botoes(self):
        botoes_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=10, pady=10)
        
        # Botão Salvar
        self.salvar_btn = ctk.CTkButton(
            botoes_frame,
            text="Salvar",
            command=self.salvar_desligamento,
            width=120,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.salvar_btn.pack(side="left", padx=5, expand=True)
        
        # Botão Limpar
        self.limpar_btn = ctk.CTkButton(
            botoes_frame,
            text="Limpar",
            command=self.limpar_campos,
            width=120,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.limpar_btn.pack(side="left", padx=5, expand=True)
        
    def carregar_opcoes_motivo(self):
        motivos = [
            "Pedido de Demissão",
            "Demissão Sem Justa Causa",
            "Demissão Com Justa Causa",
            "Término de Contrato",
            "Acordo Entre as Partes"
        ]
        self.motivo_combobox.configure(values=motivos)
        self.motivo_combobox.set(motivos[0])
        
    def buscar_funcionario(self):
        matricula = self.matricula_entry.get()
        if not matricula:
            messagebox.showerror("Erro", "Por favor, insira uma matrícula")
            return
            
        funcionario = self.db.buscar_por_matricula(matricula)
        if funcionario:
            self.nome_entry.configure(state="normal")
            self.nome_entry.delete(0, "end")
            self.nome_entry.insert(0, funcionario[1])
            self.nome_entry.configure(state="disabled")
            
            self.cargo_entry.configure(state="normal")
            self.cargo_entry.delete(0, "end")
            self.cargo_entry.insert(0, funcionario[2])
            self.cargo_entry.configure(state="disabled")
            
            self.setor_entry.configure(state="normal")
            self.setor_entry.delete(0, "end")
            self.setor_entry.insert(0, funcionario[3])
            self.setor_entry.configure(state="disabled")
            
            # Formata a data de admissão
            data_admissao = datetime.strptime(funcionario[8], '%Y-%m-%d').strftime('%d/%m/%Y')
            
            self.admissao_entry.configure(state="normal")
            self.admissao_entry.delete(0, "end")
            self.admissao_entry.insert(0, data_admissao)
            self.admissao_entry.configure(state="disabled")
        else:
            messagebox.showerror("Erro", "Funcionário não encontrado")
            
    def salvar_desligamento(self):
        try:
            matricula = self.matricula_entry.get()
            if not matricula:
                messagebox.showerror("Erro", "Por favor, insira uma matrícula")
                return
            
            # Preparar dados para inserção
            dados_funcionario = (
                matricula,
                self.nome_entry.get().upper(),
                self.cargo_entry.get().upper(),
                self.setor_entry.get().upper()
            )
            
            motivo = self.motivo_combobox.get()
            observacao = self.observacao_text.get("1.0", "end-1c")
            
            # Inserir na tabela de desligados com todos os dados
            self.db.inserir_desligamento(dados_funcionario, motivo, observacao)
            
            # Deletar da tabela de funcionários
            self.db.deletar(matricula)
            
            messagebox.showinfo("Sucesso", "Desligamento registrado com sucesso!")
            self.limpar_campos()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar desligamento: {str(e)}")
            
    def limpar_campos(self):
        self.matricula_entry.delete(0, "end")
        self.nome_entry.configure(state="normal")
        self.nome_entry.delete(0, "end")
        self.nome_entry.configure(state="disabled")
        self.cargo_entry.configure(state="normal")
        self.cargo_entry.delete(0, "end")
        self.cargo_entry.configure(state="disabled")
        self.setor_entry.configure(state="normal")
        self.setor_entry.delete(0, "end")
        self.setor_entry.configure(state="disabled")
        self.admissao_entry.configure(state="normal")
        self.admissao_entry.delete(0, "end")
        self.admissao_entry.configure(state="disabled")
        self.observacao_text.delete("1.0", "end")
        self.motivo_combobox.set(self.motivo_combobox._values[0])

if __name__ == "__main__":
    app = RegistroDesligamento()
    app.root.mainloop()