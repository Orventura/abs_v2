import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        # Obtém o diretório atual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define o caminho para o diretório data
        data_dir = os.path.join(os.path.dirname(current_dir), 'data')
        
        # Garante que o diretório data existe
        os.makedirs(data_dir, exist_ok=True)
        
        # Define o caminho completo para o banco de dados
        db_path = os.path.join(data_dir, 'funcionarios.db')
        
        # Cria/conecta ao banco de dados
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.criar_tabela()
    
    def criar_tabela(self):
        # Tabela de funcionários (já existente)
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
            pcd TEXT,
            observacoes TEXT
        )
        """)

        # Nova tabela de ocorrências
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ocorrencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            area TEXT NOT NULL,
            turno TEXT NOT NULL,
            matricula TEXT NOT NULL,
            colaborador TEXT NOT NULL,
            tipo_ausencia TEXT NOT NULL,
            observacao TEXT,
            justificado TEXT NOT NULL,
            FOREIGN KEY (matricula) REFERENCES funcionarios(mat)
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
    
    def buscar_dados_funcionario_para_ocorrencia(self, matricula):
        """Busca os dados relevantes do funcionário para a ocorrência"""
        self.cursor.execute("""
        SELECT mat, nome, area, turno 
        FROM funcionarios 
        WHERE mat = ?
        """, (matricula,))
        return self.cursor.fetchone()

    def inserir_ocorrencia(self, dados):
        """Insere uma nova ocorrência"""
        self.cursor.execute("""
        INSERT INTO ocorrencias (
            data, area, turno, matricula, colaborador,
            tipo_ausencia, observacao, justificado
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
        self.conn.commit()

    def buscar_ocorrencias(self, matricula=None):
        """Busca ocorrências, opcionalmente filtradas por matrícula"""
        if matricula:
            self.cursor.execute("SELECT * FROM ocorrencias WHERE matricula = ?", (matricula,))
        else:
            self.cursor.execute("SELECT * FROM ocorrencias")
        return self.cursor.fetchall()
    
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
        "42",          # sapato
        "Não",         # pcd
        "Ativo"        # observacoes
    )

    print("\n=== Teste do Banco de Dados ===")
    
    # Teste 1: Inserção
    try:
        print("\n1. Testando inserção...")
        db.inserir(funcionario_teste)
        print("✅ Inserção realizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro na inserção: {e}")

    # Teste 2: Consulta total
    try:
        print("\n2. Testando consulta total...")
        funcionarios = db.buscar_todos()
        print(f"✅ {len(funcionarios)} registros encontrados.")
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

def teste_aniversariantes():
    db = Database()
    
    # Limpa a tabela de funcionários antes do teste
    db.cursor.execute("DELETE FROM funcionarios")
    db.conn.commit()

    # Dados de exemplo para teste
    funcionarios_teste = [
        ("12345", "João Silva", "Operador", "Produção", "Empresa A", "1º Turno", "Área 1", "Maria Souza", "2025-01-16", "2025-01-16", "123.456.789-00", "joao@email.com", "Rua A, 123", "Centro", "Próximo ao mercado", "(11)99999-9999", "(11)88888-8888", "Rota 1", "M", "42", "Não", "Ativo"),
        ("12346", "Maria Oliveira", "Analista", "Financeiro", "Empresa B", "2º Turno", "Área 2", "Carlos Santos", "2024-01-15", "1995-01-13", "987.654.321-00", "maria@email.com", "Rua B, 456", "Centro", "Próximo ao shopping", "(11)99999-8888", "(11)88888-7777", "Rota 2", "G", "40", "Não", "Ativo"),
        ("12347", "Pedro Almeida", "Gerente", "Vendas", "Empresa C", "3º Turno", "Área 3", "Ana Lima", "2024-01-15", "1988-02-25", "456.789.123-00", "pedro@email.com", "Rua C, 789", "Centro", "Próximo ao parque", "(11)99999-7777", "(11)88888-6666", "Rota 3", "P", "44", "Não", "Ativo"),
    ]

    # Inserindo os dados de teste
    for funcionario in funcionarios_teste:
        try:
            db.inserir(funcionario)
            print(f"✅ Inserção de {funcionario[1]} realizada com sucesso!")
        except Exception as e:
            print(f"❌ Erro na inserção de {funcionario[1]}: {e}")

    # Verifica se os dados foram inseridos corretamente
    funcionarios = db.buscar_todos()
    print(f"Total de funcionários no banco de dados após inserção: {len(funcionarios)}")

    # Testando a busca de aniversariantes
    print("\n=== Testando Aniversariantes ===")
    hoje = datetime.now()
    mes_atual = hoje.month
    dia_atual = hoje.day

    # Filtra os aniversariantes do mês
    aniversariantes = []
    for funcionario in funcionarios:
        nome = funcionario[1]
        data_nascimento = funcionario[9]  # Assume que a data de nascimento está na posição 10
        print(f"Verificando {nome} com data de nascimento {data_nascimento}")  # Debug print
        if data_nascimento:
            try:
                ano_nascimento, mes_nascimento, dia_nascimento = map(int, data_nascimento.split('-'))
                if mes_nascimento == mes_atual:
                    aniversariantes.append((nome, data_nascimento, dia_nascimento == dia_atual))
            except ValueError:
                print(f"Data de nascimento inválida para {nome}: {data_nascimento}")

    # Exibe os aniversariantes encontrados
    if aniversariantes:
        print("Aniversariantes do Mês:")
        for nome, data, is_today in aniversariantes:
            emoji = " 🎉🎂" if is_today else ""
            print(f"{nome} - {data}{emoji}")
    else:
        print("Nenhum aniversariante encontrado para este mês.")

if __name__ == "__main__":
    db = Database()
    teste_banco()
    teste_aniversariantes()
    