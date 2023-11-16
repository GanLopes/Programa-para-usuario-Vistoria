import oracledb

def obter_connection():
    try:
        connection = oracledb.connect(user="******", password="******", dsn="*****")
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

# Função com inserts no banco
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

#CRUD

# Menu onde o usuario escolhe oque desaja fazer após realizar o login (inserir, atualizar, deletar, listar_bicicletas )
def menu_crud():
    while True:
            print ('''
===============OQUE DESEJA FAZER==============
(1) Inserir bike
(2) Atualizar bike
(3) Deletar bike
(4) Listar Bike
(5) Sair
==============================================''')
            try:
                escolha_crud = int(input("Escolha: "))
                list_escolha = (1, 2, 3, 4, 5)
                if escolha_crud in list_escolha:
                    return escolha_crud
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print ("Valor de entrada incorreta. Tente novamente.")

# Função que o usuario pode inserir outra bike caso ja tenha cadastro
def inserir_nova_bike(id_cliente, bike, acessorios):
    try:
        connection = obter_connection()
        cursor_bike = connection.cursor()

        # Adicione esta linha para imprimir os dados da bicicleta a serem inseridos
        print(f"Dados da bicicleta a serem inseridos: {bike}")

        # Inserção dos dados da bicicleta    
        sql_query_bike = """
            INSERT INTO T_MGT_BIKE (ID_CLIENTE, ID_BIKE, NM_MARCA, NR_REGISTRO, NM_COR, DT_BIKE, VL_MERCADO, TP_FUNCAO, TP_MODELO)
            VALUES (:id_cliente, SEQ_ID_BIKE.NEXTVAL, :marca, :registro, :cor, :data_bike, :valor_mercado, :funcao, :modelo)
        """
        cursor_bike.execute(sql_query_bike, {
            'id_cliente': id_cliente,
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
        print(f"Erro ao inserir dados da bicicleta: {e}")
        connection.rollback()
    finally:
        cursor_bike.close()

    try:
        cursor_acessorio = connection.cursor()

        # Adicione esta linha para imprimir os dados do acessório a serem inseridos
        print(f"Dados do acessório a serem inseridos: {acessorios}")

        # Inserção dos dados do acessório    
        sql_query_acessorio = """
            INSERT INTO T_MGT_ACESSORIO (ID_ACESSORIO, ID_BIKE, NM_ACESSORIO, VL_ACESSORIO)
            VALUES (SEQ_ID_ACESSORIO.NEXTVAL, SEQ_ID_BIKE.CURRVAL, :acessorio, :preco)
        """
        for acessorio in acessorios:
            cursor_acessorio.execute(sql_query_acessorio, {
                'acessorio': acessorio['Acessório'],
                'preco': acessorio['Preço'],
            })
        connection.commit()
        print("Dados do acessório inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados do acessório: {e}")
        connection.rollback()
    finally:
        cursor_acessorio.close()
        close_connection(connection)

# Função que o usuario pode atualizar outra bike caso ja tenha cadastro
def atualizar(numeracao):
    try:
        connection = obter_connection()
        cursor = connection.cursor()

        updates = {}
        print("Escolha os campos que deseja atualizar:")
        print("1. Marca")
        print("2. Registro")
        print("3. Cor")
        print("4. Data")
        print("5. Valor")
        print("6. Função")
        print("7. Modelo")

        escolha = input("Informe os números dos campos separados por vírgula (caso queira alterar mais de um): ").split(",")

        if "1" in escolha:
            updates["NM_MARCA"] = input("Nova marca: ")
        elif "2" in escolha:
            updates["NR_REGISTRO"] = input("Novo registro: ")
        elif "3" in escolha:
            updates["NM_COR"] = input("Nova cor: ")
        elif "4" in escolha:
            updates["DT_BIKE"] = input("Nova data: ")
        elif "5" in escolha:
            updates["VL_MERCADO"] = input("Novo valor: ")
        elif "6" in escolha:
            updates["TP_FUNCAO"] = input("Nova função: ")
        elif "7" in escolha:
            updates["TP_MODELO"] = input("Novo modelo: ")

        update_query = "UPDATE T_MGT_BIKE SET "
        update_query += ", ".join([f"{key} = :{key}" for key in updates.keys()])
        update_query += " WHERE NR_REGISTRO = :numeracao"

        updates["numeracao"] = numeracao

        # ** é usado para desempacotar o dicionario updates.
        cursor.execute(update_query, **updates)
        connection.commit()
        print("Bicicleta atualizada com sucesso!")
    except ValueError:
        print("Número inválido. Certifique-se de inserir um número inteiro.")
    except Exception as e:
        print(f"Erro ao atualizar bicicleta: {e}")
    finally:
        cursor.close()
        close_connection(connection)

# Consulta para obter o id_bike pelo número de série
def obter_id_bike(numero_serie):
    try:
        connection = obter_connection()
        cursor = connection.cursor()

        # Consulta para obter o id_bike pelo número de série
        query = "SELECT ID_BIKE FROM T_MGT_BIKE WHERE NR_REGISTRO = :nr_registro"
        cursor.execute(query, {"nr_registro": numero_serie})

        # Recupera o resultado da consulta
        result = cursor.fetchone()

        if result:
            id_bike = result[0]
            return id_bike
        else:
            print(f"Bicicleta com número de série {numero_serie} não encontrada.")
            return None

    except Exception as e:
        print(f"Erro ao obter id_bike pelo número de série: {e}")
    finally:
        cursor.close()
        close_connection(connection)

# Função que o usuario pode deletar outra bike caso ja tenha cadastro
def deletar(numeracao):
    try:
        connection = obter_connection()
        cursor = connection.cursor()

        id_bike = obter_id_bike(numeracao)

        # Inicia uma transação
        connection.begin()

        # Delete acessórios relacionados à bicicleta
        delete_acessorios_query = "DELETE FROM T_MGT_ACESSORIO WHERE ID_BIKE = :id_bike"
        cursor.execute(delete_acessorios_query, {"id_bike": id_bike})

        # Delete a bicicleta
        delete_bicicleta_query = "DELETE FROM T_MGT_BIKE WHERE NR_REGISTRO  = :numeracao"
        cursor.execute(delete_bicicleta_query, numeracao=numeracao)

        connection.commit()

        print("Bike e acessorios escluidos com sucesso")
    except ValueError:
        print("Número inválido. Certifique-se de inserir um número inteiro.")
    except Exception as e:
        print(f"Erro ao deletar bicicleta e acessórios: {e}")
    finally:
        cursor.close()
        close_connection(connection)

# Função para pear o id do cliente pelo do cpf 
def obter_id_cliente(cpf):
    try:
        connection = obter_connection()
        cursor = connection.cursor()

        # Consulta para obter o ID do cliente pelo CPF
        cursor.execute("SELECT ID_CLIENTE FROM T_MGT_PESSOA_FISICA WHERE NR_CPF = :cpf", cpf=cpf)

        # Recupera o ID do cliente
        id_cliente = cursor.fetchone()

        if id_cliente:
            return id_cliente[0]
        else:
            return None  # Se nenhum cliente encontrado

    except Exception as e:
        print(f"Erro ao obter ID do cliente por CPF: {e}")
    finally:
        cursor.close()
        close_connection(connection)

# Lista a bike do usuario que esta logado
def listar_bike(cpf):
    connection = None
    cursor = None
    try:
        # Obtenha o ID do usuário pelo CPF
        id_usuario = obter_id_cliente(cpf)

        if id_usuario is not None:
            connection = obter_connection()
            cursor = connection.cursor()

            # Consulta para listar bicicletas do usuário específico
            cursor.execute("SELECT * FROM T_MGT_BIKE WHERE ID_CLIENTE = :id_usuario", id_usuario=id_usuario)

            # Recupera todos os registros
            bicicletas = cursor.fetchall()

            if bicicletas:
                print(f"Lista de bicicletas para o usuário com CPF {cpf}:")
                for bicicleta in bicicletas:
                    print(f"Marca: {bicicleta[2]}")
                    print(f"Numeracao: {bicicleta[3]}")
                    print(f"Cor: {bicicleta[4]}")
                    print(f"Ano bike: {bicicleta[5]}")
                    print(f"valor_mercado: {bicicleta[6]}")
                    print(f"funcao: {bicicleta[7]}")
                    print(f"modelo: {bicicleta[8]}")
            else:
                print(f"Nenhuma bicicleta encontrada para o usuário com CPF {cpf}.")

        else:
            print(f"Usuário não encontrado para o CPF {cpf}.")

    except Exception as e:
        print(f"Erro ao listar bicicletas: {e}")
    finally:
        cursor.close()
        close_connection(connection)
