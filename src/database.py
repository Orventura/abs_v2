import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name='funcionarios.db'):
        # Obtém o diretório atual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define o caminho para o diretório data
        data_dir = os.path.join(os.path.dirname(current_dir), 'data')
        
        # Garante que o diretório data existe
        os.makedirs(data_dir, exist_ok=True)
        
        # Define o caminho completo para o banco de dados
        self.db_path = os.path.join(data_dir, db_name)
        
        # Cria/conecta ao banco de dados
        self.conn = sqlite3.connect(self.db_path)
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
        
        # Tabela de férias
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ferias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT NOT NULL,
            nome TEXT NOT NULL,
            funcao TEXT NOT NULL,
            cc TEXT,
            desc_cc TEXT,
            dt_admissao TEXT NOT NULL,
            dt_inicio TEXT NOT NULL,
            dt_retorno TEXT NOT NULL,
            dias_gozo INTEGER NOT NULL,
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
    
    def inserir_ferias(self, dados):
        self.cursor.execute("""
        INSERT INTO ferias (
            matricula, nome, funcao, cc, desc_cc,
            dt_admissao, dt_inicio, dt_retorno, dias_gozo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
        self.conn.commit()

    def buscar_ferias(self, matricula=None):
        if matricula:
            self.cursor.execute("SELECT * FROM ferias WHERE matricula = ?", (matricula,))
        else:
            self.cursor.execute("SELECT * FROM ferias")
        return self.cursor.fetchall()

    def atualizar_ferias(self, dados):
        query = """
            UPDATE ferias 
            SET nome = ?, 
                funcao = ?, 
                cc = ?, 
                desc_cc = ?, 
                dt_admissao = ?, 
                dt_inicio = ?, 
                dt_retorno = ?, 
                dias_gozo = ?
            WHERE matricula = ?
        """
        self.cursor.execute(query, dados)
        self.conn.commit()

    def deletar_ferias(self, id):
        self.cursor.execute("DELETE FROM ferias WHERE id=?", (id,))
        self.conn.commit()

    def buscar_ferias_funcionario(self, matricula):
        self.cursor.execute("""
        SELECT cc, desc_cc, dt_inicio, dt_retorno, dias_gozo 
        FROM ferias 
        WHERE matricula = ? 
        ORDER BY dt_inicio DESC 
        LIMIT 1""", (matricula,))
        return self.cursor.fetchone()

    def __del__(self):
        self.conn.close()

def teste_banco():
    # Criar uma instância do banco de dados de teste
    db = Database('teste.db')
    
    # Dados de exemplo para teste
    funcionario_teste = (
        "12345",        # mat
        "João Silva",   # nome
        "Operador",     # cargo
        "Produção",     # setor
        "Empresa A",    # empresa
        "1º Turno",     # turno
        "Área 1",       # area
        "Maria Souza",  # lider
        "2023-01-15",   # dt_admissao
        "1990-01-15",   # dt_nascimento
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

    # Teste de aniversariantes
    funcionarios_aniversariantes = [
        ("12346", "Maria Oliveira", "Analista", "RH", "Empresa B", "2º Turno", "Área 2", "João Silva", 
         "2023-02-15", datetime.now().strftime('%Y-%m-%d'), "987.654.321-00", "maria@email.com",
         "Rua B, 456", "Centro", "Próximo à escola", "(11)77777-7777", "(11)66666-6666",
         "Rota 2", "P", "38", "Não", "Ativo"),
        ("12347", "Pedro Santos", "Gerente", "Administrativo", "Empresa C", "1º Turno", "Área 3", "Ana Silva",
         "2023-03-15", "1985-12-25", "456.789.123-00", "pedro@email.com", "Rua C, 789", "Centro",
         "Próximo ao parque", "(11)55555-5555", "(11)44444-4444", "Rota 3", "G", "41", "Não", "Ativo")
    ]

    print("\n=== Teste do Banco de Dados ===")
    
    # Teste 1: Inserção do funcionário de teste
    try:
        print("\n1. Testando inserção do funcionário de teste...")
        db.inserir(funcionario_teste)
        print("✅ Inserção realizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro na inserção: {e}")

    # Teste 2: Inserção dos funcionários para teste de aniversariantes
    try:
        print("\n2. Testando inserção dos funcionários para teste de aniversariantes...")
        for func in funcionarios_aniversariantes:
            db.inserir(func)
        print("✅ Inserção dos funcionários para teste de aniversariantes realizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro na inserção dos funcionários para teste de aniversariantes: {e}")

    # Teste 3: Consulta de aniversariantes
    try:
        print("\n3. Testando consulta de aniversariantes...")
        hoje = datetime.now()
        mes_atual = hoje.month
        dia_atual = hoje.day
        
        funcionarios = db.buscar_todos()
        aniversariantes = []
        
        for funcionario in funcionarios:
            nome = funcionario[1]
            data_nascimento = funcionario[9]
            
            if data_nascimento:
                try:
                    ano_nascimento, mes_nascimento, dia_nascimento = map(int, data_nascimento.split('-'))
                    if mes_nascimento == mes_atual:
                        aniversariantes.append((nome, data_nascimento, dia_nascimento == dia_atual))
                except ValueError:
                    print(f"Data de nascimento inválida para {nome}: {data_nascimento}")
        
        if aniversariantes:
            print("\nAniversariantes do Mês:")
            for nome, data, is_today in aniversariantes:
                emoji = "🎉🎂" if is_today else ""
                print(f"{nome} - {data} {emoji}")
        else:
            print("Nenhum aniversariante encontrado para este mês.")
        
        print("✅ Consulta de aniversariantes realizada com sucesso!")
    except Exception as e:
        print(f"❌ Erro na consulta de aniversariantes: {e}")

    # Teste 4: Limpeza do banco de dados de teste
    try:
        print("\n4. Limpando banco de dados de teste...")
        db.conn.close()
        os.remove(db.db_path)
        print("✅ Banco de dados de teste removido com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao remover banco de dados de teste: {e}")

if __name__ == "__main__":
    db = Database()
    teste_banco()
    