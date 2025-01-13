class Validacoes:
    @staticmethod
    def validar_campos_obrigatorios(dados):
        campos_obrigatorios = {
            'mat': 'Matrícula',
            'nome': 'Nome',
            'cargo': 'Cargo',
            'setor': 'Setor',
            'empresa': 'Empresa',
            'turno': 'Turno',
            'area': 'Área',
            'lider': 'Líder',
            'dt_admissao': 'Data de Admissão',
            'dt_nascimento': 'Data de Nascimento',
            'cpf': 'CPF',
            'email': 'E-mail',
            'endereco': 'Endereço',
            'bairro': 'Bairro',
            'referencia': 'Referência',
            'telefone': 'Telefone',
            'tel_recado': 'Telefone Recado',
            'num_rota': 'Número da Rota',
            'colete': 'Colete',
            'sapato': 'Sapato',
            'observacao': 'Observação'
        }
        
        campos_vazios = []
        for campo, nome in campos_obrigatorios.items():
            if campo in ['dt_admissao', 'dt_nascimento']:
                continue  # Pula a validação de campos de data, pois sempre terão valor
            elif not dados[campo] or str(dados[campo]).strip() == '':
                campos_vazios.append(nome)
                
        return campos_vazios
    
    @staticmethod
    def validar_cpf(cpf):
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
            
        # Verifica se todos os dígitos são iguais
        if len(set(cpf)) == 1:
            return False
            
        # Validação do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if int(cpf[9]) != digito:
            return False
            
        # Validação do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if int(cpf[10]) != digito:
            return False
            
        return True
    
    @staticmethod
    def validar_email(email):
        if not email:  # Se o email estiver vazio, considera válido
            return True
            
        # Validação básica de email
        import re
        padrao = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(padrao.match(email))
    
    @staticmethod
    def validar_telefone(telefone):
        if not telefone:  # Se o telefone estiver vazio, considera válido
            return True
            
        # Remove caracteres não numéricos
        telefone = ''.join(filter(str.isdigit, telefone))
        
        # Verifica se tem entre 10 e 11 dígitos (com ou sem DDD)
        return len(telefone) in [10, 11]
