import sqlite3
from pathlib import Path

class Database:
    def __init__(self):
        # Garante que o diretório data existe
        Path("data").mkdir(exist_ok=True)
        
        # Cria/conecta ao banco de dados
        self.conn = sqlite3.connect('data/funcionarios.db')
        self.cursor = self.conn.cursor()
        self.criar_tabela()
    
    def criar_tabela(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            mat TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            cargo TEXT,
            setor TEXT,
            empresa TEXT,
            turno TEXT,
            area TEXT,
            lider TEXT,
            dt_admissao TEXT,
            dt_nascimento TEXT,
            cpf TEXT,
            email TEXT,
            endereco TEXT,
            bairro TEXT,
            referencia TEXT,
            telefone TEXT,
            tel_recado TEXT,
            num_rota TEXT,
            colete TEXT,
            sapato TEXT,
            pcd BOOLEAN,
            observacoes TEXT
        )
        """)
        self.conn.commit()
    
    def inserir(self, dados):
        self.cursor.execute("""
        INSERT INTO funcionarios (
            mat, nome, cargo, setor, empresa, turno, area, lider,
            dt_admissao, dt_nascimento, cpf, email, endereco, bairro,
            referencia, telefone, tel_recado, num_rota, colete, sapato,
            pcd, observacoes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
        self.conn.commit()
    
    def buscar_todos(self):
        self.cursor.execute("SELECT * FROM funcionarios")
        return self.cursor.fetchall()
    
    def buscar_por_matricula(self, mat):
        self.cursor.execute("SELECT * FROM funcionarios WHERE mat=?", (mat,))
        return self.cursor.fetchone()
    
    def atualizar(self, dados):
        self.cursor.execute("""
        UPDATE funcionarios 
        SET nome=?, cargo=?, setor=?, empresa=?, turno=?, area=?, lider=?,
            dt_admissao=?, dt_nascimento=?, cpf=?, email=?, endereco=?, bairro=?,
            referencia=?, telefone=?, tel_recado=?, num_rota=?, colete=?, sapato=?,
            pcd=?, observacoes=?
        WHERE mat=?
        """, dados[1:] + (dados[0],))
        self.conn.commit()
    
    def deletar(self, mat):
        self.cursor.execute("DELETE FROM funcionarios WHERE mat=?", (mat,))
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()

def teste_banco():
    db = Database()
    
    # Dados de exemplo
    funcionario_teste = (
        "12345",        # mat
        "João Silva",   # nome
        "Operador",     # cargo
        "Produção",     # setor
        "Empresa A",    # empresa
        "1º Turno",     # turno
        "Área 1",       # area
        "Maria Souza",  # lider
        "2024-01-15",   # dt_admissao
        "1990-05-20",   # dt_nascimento
        "123.456.789-00", # cpf
        "joao@email.com", # email
        "Rua A, 123",   # endereco
        "Centro",       # bairro
        "Próximo ao mercado", # referencia
        "(11)99999-9999", # telefone
        "(11)88888-8888", # tel_recado
        "Rota 1",      # num_rota
        "M",           # colete
        "42"           # sapato
    )

    print("\n=== Teste do Banco de Dados ===")
    
    # Teste 1: Inserção
    try:
        print("\n1. Testando inserção...")
        db.inserir(funcionario_teste)
        print("✅ Inserção realizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro na inserção: {e}")

    # Teste 2: Consulta todos
    try:
        print("\n2. Testando consulta geral...")
        funcionarios = db.buscar_todos()
        print(f"✅ Consulta realizada com sucesso! {len(funcionarios)} registros encontrados.")
    except Exception as e:
        print(f"❌ Erro na consulta geral: {e}")

    # Teste 3: Consulta específica
    try:
        print("\n3. Testando consulta por matrícula...")
        funcionario = db.buscar_por_matricula("12345")
        if funcionario:
            print("✅ Consulta por matrícula realizada com sucesso!")
            print(f"   Nome encontrado: {funcionario[1]}")
    except Exception as e:
        print(f"❌ Erro na consulta por matrícula: {e}")

    # Teste 4: Atualização
    funcionario_atualizado = list(funcionario_teste)
    funcionario_atualizado[1] = "João Silva Junior"  # Alterando o nome
    try:
        print("\n4. Testando atualização...")
        db.atualizar(tuple(funcionario_atualizado))
        print("✅ Atualização realizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro na atualização: {e}")

    # Teste 5: Verificar atualização
    try:
        print("\n5. Verificando atualização...")
        funcionario = db.buscar_por_matricula("12345")
        if funcionario and funcionario[1] == "João Silva Junior":
            print("✅ Atualização confirmada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao verificar atualização: {e}")

    # Teste 6: Exclusão
    try:
        print("\n6. Testando exclusão...")
        db.deletar("12345")
        print("✅ Exclusão realizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro na exclusão: {e}")

if __name__ == "__main__":
    teste_banco()