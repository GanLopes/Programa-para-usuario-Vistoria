from datetime import date
import re 
import requests
from aaa import *

# Função para autenticar o usuário
def Cadastro():
    dados_cadastro = {}
    try:
        while True:
            nome = input("Nome: ")
            if valida_nome(nome):
                break
        while True:
            cpf = input("CPF: ")
            # Valida cpf
            cpf_digitos = [int(c) for c in cpf if c.isdigit()] 
            if Verifica_cpf(cpf_digitos):
                break
            else:
                print("CPF inválido! Digite Novamente")

        while True:
            endereco = input("CEP: ")
            uf, cidade, logradouro = obter_informacoes_cep(endereco)
            if uf is not None:
                break
            else:
                print("CEP inválido ou não encontrado. Digite Novamente")

        while True:
            telefone = (input("Telefone (no formato XX XXXXXXXX ou XX XXXXXXXXX): "))
            if verifica_telefone(telefone):
                 break

        while True:
            email = input("E-mail: ")
            if verifca_email(email):
                break

        while True:
            data_nasc = input("Insira a data de nascimento (DD/MM/AAAA): ")
            if validar_data_nascimento(data_nasc):
                break

        dados_cadastro = {"Nome": nome, "Cpf": cpf, "Endereço": endereco, "UF": uf, "Cidade": cidade, "logradoro": logradouro, "Telefone": telefone, "E-mail": email,
                          "Data de Nascimento": data_nasc}
    except ValueError:
                print("Valor de entrada incorreto.")
    return dados_cadastro

# Funçao para obter alguns dados de acordo com o cep
def obter_informacoes_cep(cep):
    cep = cep.replace(".", "").replace("-", "")
    if len(cep) != 8:
        print('CEP inválido. Deve conter 8 dígitos.')
        return None, None, None

    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        requisicao = requests.get(url)
        if requisicao.status_code == 200:
            dic_requisicao = requisicao.json()
            uf = dic_requisicao.get('uf', '')
            cidade = dic_requisicao.get('localidade', '')
            logradouro = dic_requisicao.get('logradouro', '')
            
            # Se o logradouro não estiver presente, solicite ao usuário
            if not logradouro:
                print(f'Uf: {uf} \ncidade: {cidade} ')
                while True:
                    logradouro = input("Rua não encontrado. Por favor, insira o logradouro manualmente: ")
                    if valida_nome(logradouro):
                        break

            return uf, cidade, logradouro
        else:
            print('CEP não encontrado ou erro na requisição.')
            return None, None, None
    except requests.exceptions.RequestException as e:
        print(f'Erro na requisição à API: {e}')
        return None, None, None

# Verifica se o nome é valido
def valida_nome(nome):
    try:
        if nome.replace(" ", "").isalpha():
            return nome
        else:
            raise ValueError("Digite um valor válido contendo apenas letras e espaços.")
    except ValueError as e:
        print(f"Erro: {e}")
        return None

# Verificar se o cpf é valido
def Verifica_cpf(num):
    try:
        # Verifica se o dados possui 11 digitos
        if len(num) != 11:
            return False

        soma = 0
        j = 10
        # Percorre os 9 digitos
        for i in range(9):
            soma += num[i] * j
            j -= 1
        resto = soma % 11
        if resto < 2:
            dv1 = 0
        else:
            dv1 = 11 - resto
        # Dígito verificador #2
        soma = 0
        j = 11
        for i in range(10):
            soma += num[i] * j
            # Toda vez que passa aqui subtrai 1
            j -= 1
        resto = soma % 11
        if resto < 2:
            dv2 = 0
        else:
            dv2 = 11 - resto
        if num[9] == dv1 and num[10] == dv2:
            return True
        else:
            return False
    except ValueError as e:
        print(f"Erro: {e}")

# Verificar se telefone é valido
def verifica_telefone(telefone):
    try:
        # Padrão de expressão regular para validar números de telefone brasileiros
        padrao = r"^\(?\d{2}\)?\s\d{4,5}\d{4}$"

        if re.match(padrao, telefone):
            return True
        else:
            print("Número de telefone inválido.")
            return False
    except Exception as e:
        print(f"Erro: {e}")

# Verificar se email é valido
def verifca_email(email):
    try:
        # Padrão de expressão regular para validar e-mails
        padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        
        if re.match(padrao, email):
            return True
        else:         
            print("e-mail inválido. Digite Novamente")
            return False
    except Exception as e:
        print(f"Erro: {e}")

# Verifica se usuario é maior de idade
def validar_data_nascimento(data):
    while True:
        try:
            dia, mes, ano = data.split('/')
            dia = int(dia)
            mes = int(mes)
            ano = int(ano)
            data_nascimento = date(ano, mes, dia)

            if ano <= 1950:
                print("Ano de nascimento deve ser maior que 1950.")
                return None
            # Calcula a data atual
            data_atual = date.today()

            # Calcula a data há 18 anos atrás
            data_limite = data_atual.replace(year=data_atual.year - 18)

            if data_nascimento <= data_limite:
                return data_nascimento
            else:
                print("Você deve ter pelo menos 18 anos para se cadastrar.")
        except (ValueError, OverflowError):
            print("Data invalida verifique o Formato Use DD/MM/AAAA e tente novamente.")
        return None

# Validar caso o usurio coloque um valor incorreto
def validar_preenchimento(obj, valor_minimo):
    return obj >= valor_minimo
        
# Coletar dados da bike 
def coleta_dados_bike():
    while True:
        try:
            while True:
                Marca = input("Digite a Marca da bike: ")
                if valida_nome(Marca):  
                    break
                
            while True:
                Numeracao = (input("Digite a numeração da bike: "))
                break
            while True:
                cor = input("Digite a cor da bike (Ex: Amarela, Preta): ")
                if valida_nome(cor):
                    break 

            while True:
                ano_bike = int(input("Digite o ano de fabricação da bike: "))
                if not validar_preenchimento(ano_bike, date.today().year - 8) or ano_bike > date.today().year:
                    print("Ano de fabricação inválido.")
                else:
                    break

            while True:
                valor_mercado = float(input("Digite o valor de mercado da bike: "))
                if not validar_preenchimento(valor_mercado, 2000):
                    print("Valor de mercado inválido. Deve ser maior ou igual a 2000.")
                break
            
            while True:
                funcao = input("Digite a função da bike (ex: Trabalho, lazer, competição): ")
                if valida_nome(funcao):
                    break
            while True:
                modelo = input("Informe o modelo da sua bike (Ex: Bmx, Dobrável, Elétrica, Elétrica e Dobrável, Downhill, etc): ")
                if valida_nome(modelo):
                    break 
                
            bike = {"Marca": Marca, "registro": Numeracao, "Cor": cor, "Ano_bike": ano_bike , 
                    "Valor Mercado": valor_mercado, "Função": funcao, "Modelo": modelo}
            return bike
        except ValueError:
            print("Valor de entrada inválido. Certifique-se de inserir um número válido.")

# Menu para escolher se a bike possui acessórios
def menu_acessorio():
    while True:
        print('''
================== Acessórios =================
(1) Caso sua bike tenha acessórios
(2) Caso não tenha acessórios
===============================================''')
        try:
            escolha_acessorio = int(input("Escolha: "))
            list_escolha_acessorio = (1,2)

            if escolha_acessorio in list_escolha_acessorio:
                return escolha_acessorio
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
                print ("Valor de entrada incorreta. Tente novamente.")

# Coletar informações sobre acessórios
def acessorios(escolha_acessorio):
    lista_acessorios = []

    if escolha_acessorio == 1:
        i = 1
        while True:
            try:
                acessorio = input(f"Digite o {i}º acessório ('.' para encerrar): ")
                if acessorio == '.':
                    break
                preco = float(input(f"Preço do {i}º acessório ({acessorio}): "))
                if not validar_preenchimento(preco, 10):
                    print("O preço de ser acima de 10 reais")

                dict_acessorio = {"Acessório": acessorio, "Preço": preco}
                lista_acessorios.append(dict_acessorio)
                
                i += 1
            except ValueError:
                print("Preço inválido. Insira um valor numérico válido.")

    elif escolha_acessorio == 2:
        lista_acessorios.append({"Acessório": "Nenhum", "Preço": 0.0})
    else:
        print("Escolha inválida.")

    return lista_acessorios

# O fução para o usuario escoher oq deseja alterar
def menu_correçao():
    print (''' 
==============================================
(1) Corigir dados Pessoa 
(2) Corigir dados da bike 
(3) Corigir Acessorio
(4) Sair
==============================================
''')
    try:
        escolha_correção = int(input("Escolha: "))
        list_escolha = (1, 2, 3)
        if escolha_correção in list_escolha:
            return escolha_correção
        else:
            print("Escolha inválida. Tente novamente.")
    except ValueError:
                print ("Valor de entrada incorreta. Tente novamente.")

# Função para corrigir dados do usuário 
def corrigir_dados(escolha_acessorio, dados_bike, daodos_cadastro, lista_acessorios ):
    while True:
        try:
            print('Os dados estão corretos S/N')
            correcao = input("Escolha: ")
            if correcao == 'N' or correcao == 'n':
                escolha_correção = menu_correçao()
                if escolha_correção == 1:
                    daodos_cadastro = Cadastro()
                elif escolha_correção == 2:
                    dados_bike = coleta_dados_bike()
                elif escolha_correção == 3:
                    lista_acessorios = acessorios(escolha_acessorio)
                elif escolha_correção == 4:
                    exit()
                else:
                    print("Etapa finalizada")
                exibir_dados(daodos_cadastro, dados_bike, lista_acessorios)
            else:
                print("Ok, Etapa concluida")
                break
        except ValueError as e:
            print("Dado de entrada invalido!")

# Função para somor a proço dos acessorios e da bike
def calcular_preco_total(dados):
    preco_total = 0.0
    for bike in dados:
        valor_mercado = bike.get("Valor Mercado", 0.0)  # pegar valor de mercado da bike
        acessorios = bike.get("Acessórios", [])  # pegar lista de acessórios 
        preco_acessorios = sum(acessorio.get("Preço", 0.0) for acessorio in acessorios)  # Soma os preços dos acessórios
        preco_total += valor_mercado + preco_acessorios  # Adiciona o valor de mercado e o preço dos acessórios

    return preco_total

# Exibir os dados da bike e acessórios
def exibir_dados(dados_cadastro, dados_bike, lista_acessorios):
    print("\nDADOS CADASTRO")
    for key, value in dados_cadastro.items():
        print(f"{key}: {value}")

    print("\nDADOS DA BIKE")
    dados_bike["Acessórios"] = lista_acessorios
    for chave, valor in dados_bike.items():
            print(f"{chave}: {valor}")

    preco_total = calcular_preco_total([dados_bike]) 
    print(f"\nPreço total da bicicleta com acessórios: R${preco_total:.2f}")

# Função principal para realizar cadastro
def principal_cadatro():
    # coletar dados cadastro
    print("Insira os dados para o cadastro")
    daodos_cadastro = Cadastro()
    # Coleta dados sobre bicicletas
    print("Insira os dados da bike")
    dados_bike = coleta_dados_bike()

    escolha_acessorio = menu_acessorio()
    # Coleta informações sobre os acessórios
    lista_acessorios = acessorios(escolha_acessorio)
    # Exibe dados cadastrados
    exibir_dados(daodos_cadastro, dados_bike, lista_acessorios)
    corrigir_dados(escolha_acessorio, dados_bike,daodos_cadastro,  lista_acessorios)
    # Insere os dados no banco de dados oracle
    insert(daodos_cadastro, dados_bike, lista_acessorios)

# Menu onde usuario pode escolher se desaja se cadastra em nosso site ou realizar login
def opcao():
    while True:
        print('''
======= INFORME COMO DESEJA LOGAR NO SITE =======
(1) Login
(2) Cadastro
(3) Sair
==============================================''')
        try:
            escolha_entrada = int(input("Escolha: "))
            if  escolha_entrada in (1, 2, 3):
                return  escolha_entrada
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Valor de entrada incorreto. Tente novamente.")

# Função para verificar se o usuario já esta cadastrado 
def autenticar_cliente(nome, cpf):
    connection = obter_connection()
    cursor = connection.cursor()
    
    try:
        # Consulta para verificar se o nome e CPF correspondem
        cursor.execute("""
            SELECT * FROM T_MGT_PESSOA_FISICA
            WHERE NM_USUARIO = :nome AND NR_CPF = :cpf
        """, {'nome': nome, 'cpf': cpf})
        
        resultado = cursor.fetchone()

        if resultado:
            return True  
        else:
            return False 
    finally:
        cursor.close()
        close_connection(connection)

# Funçao onde o usuario digitas as informaloes nescessaria para o login
def login():
    while True:
        try:
            nome = input("Nome de usuário: ")
            cpf = int(input("CPF: "))
            if autenticar_cliente(nome, cpf):
                print("Autenticação bem-sucedida. Você está logado.")
                return cpf  # Retorna apenas o CPF
            else:
                print("Autenticação falhou. Por favor, tente novamente.")
        except ValueError:
            print("Erro: CPF deve ser um número inteiro. Tente novamente.")

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
        connection.close()

# Função que o usuario pode atualizar outra bike caso ja tenha cadastro
def atualizar(numeracao):
    try:
        connection = obter_connection()
        cursor = connection.cursor()

        print("Escolha os campos que deseja atualizar:")
        print("1. Marca")
        print("2. Registro")
        print("3. Cor")
        print("4. Data")
        print("5. Valor")
        print("6. Função")
        print("7. Modelo")

        escolha = input("Informe os números dos campos separados por vírgula (caso queira alterar mais de um): ").split(",")

        updates = {}

        if escolha == "1":
            updates["NM_MARCA"] = input("Nova marca: ")
        elif escolha == "2":
            updates["NR_REGISTRO"] = input("Novo registro: ")
        elif escolha == "3":
            updates["NM_COR"] = input("Nova cor: ")
        elif escolha == "4":
            updates["DT_BIKE"] = input("Nova data: ")
        elif escolha == "5":
            updates["VL_MERCADO"] = input("Novo valor: ")
        elif escolha == "6":
            updates["TP_FUNCAO"] = input("Nova função: ")
        elif escolha == "7":
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
        connection.close()

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
        connection.close()

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

        # Commit da transação
        connection.commit()

        print("Bicicleta e acessórios deletados com sucesso!")
    except ValueError:
        print("Número inválido. Certifique-se de inserir um número inteiro.")
    except Exception as e:
        print(f"Erro ao deletar bicicleta e acessórios: {e}")
    finally:
        cursor.close()
        connection.close()

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
        connection.close()

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
        connection.close()

def exibir_dados_nova_bike(dados_bike, lista_acessorios):
    print("\nDADOS DA BIKE")
    dados_bike["Acessórios"] = lista_acessorios
    for chave, valor in dados_bike.items():
            print(f"{chave}: {valor}")

    preco_total = calcular_preco_total([dados_bike]) 
    print(f"\nPreço total da bicicleta com acessórios: R${preco_total:.2f}")

# Função que realiza as funções do crud
def realizar_crud(escolha_crud, cpf):
    id_cliente = obter_id_cliente(cpf)

    if escolha_crud == 1:
        dados_bike = coleta_dados_bike()
        escolha_acessorio = menu_acessorio()
        lista_acessorios = acessorios(escolha_acessorio)
        inserir_nova_bike (id_cliente, dados_bike, lista_acessorios)
        exibir_dados( dados_bike, lista_acessorios)
    elif escolha_crud == 2:
        numeracao_atualizar = input("Digite a numeração da bicicleta que deseja atualizar: ")
        atualizar(numeracao_atualizar)
    elif escolha_crud == 3:
        numeracao_deletar = input("Digite a numeração da bicicleta que deseja deletar: ")
        deletar(numeracao_deletar)
    elif escolha_crud == 4:
        listar_bike(cpf)
    else:
        print("Escolha inválida.")

# Menu para usuario escolher entre login 
def opcao():
    while True:
        print('''
======= INFORME COMO DESEJA LOGAR NO SITE =======
(1) Login
(2) Cadastro
(3) Sair
==============================================''')
        try:
            escolha_entrada = int(input("Escolha: "))
            if  escolha_entrada in (1, 2, 3):
                return  escolha_entrada
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Valor de entrada incorreto. Tente novamente.")

# Programa principal para relizar cadastro ou login
def principal():
        escolha_entrada = opcao()
        if escolha_entrada == 1:
            cpf = login()
            crud = menu_crud()
            realizar_crud(crud, cpf)
        elif escolha_entrada == 2:
            principal_cadatro()
        else:
            print("Escolha inválida. Tente novamente.")

principal()