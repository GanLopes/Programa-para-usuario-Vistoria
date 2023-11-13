import oracledb

def obter_connection():
    try:
        connection = oracledb.connect(user="RM99585", password="210305", dsn="oracle.fiap.com.br/orcl")
        return connection
    except Exception as e:
        print(f"Erro ao obter conexão: {e}")
        return None

def close_connection(connection):
    try:
        if connection:
            connection.close()
    except Exception as e:
        print (f"Erro ao fechar conexão:{e}" )

def insert(dados_cadastro, bike, acessorio):
    connection = obter_connection()
    cursor = connection.cursor()
# Inserir dados tabela T_MGT_CLIENTE
    try:
        sql_query = """
        INSERT INTO T_MGT_CLIENTE (TP_CLIENTE)
        VALUES ('FISICA')
        """
        cursor.execute(sql_query, {
        })
        connection.commit()
        print("Dados de CLIENTE inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados de CLIENTE na tabela: {e}")
# Inserir dados tabela T_MGT_PESSOA_FISICA
    try:
        sql_query = """
        INSERT INTO T_MGT_PESSOA_FISICA (ID_CLIENTE, NM_USUARIO, NR_CPF, NR_CEP,NM_UF, NM_LOCALIDADE, NM_LOGRADORO, NR_TELEFONE, NM_EMAIL, DT_NASCIMENTO)
        VALUES (SEQ_ID_CLIENTE.CURRVAL, :nome, :cpf, :endereco, :uf, :localidade, :logradoro, :telefone, :email, TO_DATE(:nascimento, 'DD/MM/YYYY'))
        """
        cursor.execute(sql_query, {
            'nome': dados_cadastro['Nome'],
            'cpf': dados_cadastro['Cpf'],
            'endereco': dados_cadastro['Endereço'],
            'uf': dados_cadastro['UF'],
            'localidade': dados_cadastro['Cidade'],
            'logradoro': dados_cadastro['logradoro'],
            'telefone': dados_cadastro['Telefone'],
            'email': dados_cadastro['E-mail'],
            'nascimento': dados_cadastro['Data de Nascimento']
        })
        connection.commit()
        print("Dados de pessoa física inseridos com sucesso.")
    except Exception as e:
        if "ORA-00001" in str(e):
            print("Erro: Violation of unique constraint. CPF já cadastrado.")
        else:
            print(f"Erro ao inserir dados de pessoa física na tabela: {e}")

# Inserir dados tabela T_MGT_BIKE
    try:     
        sql_query = """
            INSERT INTO T_MGT_BIKE (ID_CLIENTE, ID_BIKE, NM_MARCA, NR_REGISTRO, NM_COR, DT_BIKE, VL_MERCADO, TP_FUNCAO, TP_MODELO)
            VALUES (SEQ_ID_CLIENTE.CURRVAL, SEQ_ID_BIKE.NEXTVAL, :marca, :registro, :cor, :data_bike, :valor_mercado, :funcao, :modelo)
        """
        cursor.execute(sql_query, {
            'marca': bike['Marca'],
            'registro': bike['registro'],
            'cor': bike['Cor'],
            'data_bike': bike['Ano_bike'],
            'valor_mercado': bike['Valor Mercado'],
            'funcao': bike['Função'],
            'modelo': bike['Modelo'],
        })
        connection.commit()
        print("Dados da bicicleta inseridos com sucesso.")
    except Exception as e:
        if "ORA-00001" in str(e):
            print("Erro: Violation of unique constraint. ID_BIKE já cadastrado.")
        else:
            print(f"Erro ao inserir dados da bike na tabela: {e}")
    
# Inserir dados tabela T_MGT_ACESSORIO
    try:     
        sql_query = """
            INSERT INTO T_MGT_ACESSORIO (ID_ACESSORIO, ID_BIKE, NM_ACESSORIO, VL_ACESSORIO)
            VALUES (SEQ_ID_ACESSORIO.NEXTVAL, SEQ_ID_BIKE.CURRVAL, :acessorio, :preco)
        """
        for acessorio_dict in acessorio:
            cursor.execute(sql_query, {
                'acessorio': acessorio_dict['Acessório'],
                'preco': acessorio_dict['Preço'],
            })
        
        connection.commit()
        print("Dados dos acessórios inseridos com sucesso.")
    except Exception as e:
        if "ORA-00001" in str(e):
            print("Erro: Violation of unique constraint. ID_ACESSORIO já cadastrado.")
        else:
            print(f"Erro ao inserir dados acessorios na tabela física na tabela: {e}")

    close_connection(connection)
