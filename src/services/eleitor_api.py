from services.database import ELEITORES
import sqlite3
import requests
import json

conexao = sqlite3.connect("desenvolvimento.db", check_same_thread=False)
cursor = conexao.cursor()

def consulta_eleitor(num_titulo):

    cursor.execute("""SELECT * FROM eleitores_votantes WHERE titulo_eleitor = ?""", (str(num_titulo),))
    resultado_eleitores_votantes = cursor.fetchone()
    if resultado_eleitores_votantes != None:
        if resultado_eleitores_votantes[0] == num_titulo:
            return 1
    else:
        cursor.execute("""SELECT * FROM eleitores WHERE titulo_eleitor = ?""", (str(num_titulo),))
        resultado_eleitores = cursor.fetchone()
        if resultado_eleitores != None:
            if resultado_eleitores[4] == num_titulo:
                nome = resultado_eleitores[1]
                estado = resultado_eleitores[2]
                cidade = resultado_eleitores[3]
                titulo_eleitor = resultado_eleitores[4]
                return {"nome": nome, "estado": estado, "cidade": cidade, "titulo_eleitor": titulo_eleitor}

    return 2

    # cursor.execute("""SELECT * FROM eleitores WHERE titulo_eleitor = ?""", (str(num_titulo)))
    # resultado_eleitores = cursor.fetchone()




    # print(resultado_eleitores, resultado_eleitores_votantes)

    # #for eleitor in resultado_eleitores_votantes:
    # if resultado_eleitores_votantes != None:
    #     if resultado_eleitores_votantes[0] == num_titulo:
    #         return 1

    # #for eleitor in resultado_eleitores:
    # if resultado_eleitores != None:
    #     if resultado_eleitores[-1] == num_titulo:
    #         return resultado_eleitores
    
    # return 2

def consulta_eleitor_v2(num_titulo):
    cursor.execute("""
    SELECT * FROM eleitores WHERE titulo_eleitor = ?
    """, (str(num_titulo),))
    resultados = cursor.fetchone()
    print(type(resultados))
    print(resultados)

def add_eleitor_votante(num_titulo):
    try:
        cursor.execute(f"""INSERT INTO eleitores_votantes (titulo_eleitor) VALUES ("{num_titulo}") """)
        conexao.commit()
        print("Eleitor votante salvo com sucesso!")
    except Exception as err:
        print("Não foi possivel gravar o eleitor votante!\n", err)

def retorna_cod_cidade(estado, cidade):
    cod_cidade = ""
    url_consulta_cidade = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/eleicao/buscar/{estado}/2045202024/municipios"
    response_consulta_cod_cidade = requests.get(
        url=url_consulta_cidade
    )
    for cid in response_consulta_cod_cidade.json()['municipios']:
        if cid['nome'] == str(cidade).upper():
            cod_cidade = cid['codigo']

    return cod_cidade

def retorna_lista_cidade(estado):
    lista_cidades = []
    url_consulta_cidade = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/eleicao/buscar/{estado}/2045202024/municipios"
    response_consulta_cidade = requests.get(
        url=url_consulta_cidade
    )

    for cidade in response_consulta_cidade.json()['municipios']:
        lista_cidades.append({"id": cidade['id'], "nome": cidade['nome'], "cod_cidade":cidade['codigo']})

    return lista_cidades

def retorna_lista_votos_cidade(cod_cidade):
    cursor.execute("""
    SELECT * FROM votacao WHERE cod_cidade = ?
    """, (str(cod_cidade),))

def retorna_candidatos_da_cidade(estado, cidade, votacao):
    cod_cidade = retorna_cod_cidade(estado, cidade)
    candidatos = []
    # url_consulta_cidade = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/eleicao/buscar/{estado}/2045202024/municipios"
    # response_consulta_cod_cidade = requests.get(
    #     url=url_consulta_cidade
    # )
    # for cid in response_consulta_cod_cidade.json()['municipios']:
    #     if cid['nome'] == str(cidade).upper():
    #         cod_cidade = cid['codigo']

        

    for voto in votacao:
        if voto == "vereador":
            candidatos.extend(retorna_lista_candidatos(cod_cidade, "13", estado, cidade))

        if voto == "prefeito":
            candidatos.extend(retorna_lista_candidatos(cod_cidade, "11", estado, cidade))

    return candidatos

def retorna_lista_candidatos(cod_cidade, cod_votacao, estado, cidade):
    lista_candidatos = []
    url_base = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/2024/{cod_cidade}/2045202024/{cod_votacao}/candidatos"
    response = requests.get(
        url=url_base
    )

    for candidato in response.json()["candidatos"]:
        lista_candidatos.append({"id":candidato['id'] ,"numero":candidato['numero'], "nome":candidato["nomeUrna"], "cod_cidade": cod_cidade, "estado": estado, "cidade":cidade,  "partido":candidato['partido']['sigla']})

    #print(lista_candidatos)
    return lista_candidatos

def retorna_candidato_voto(candidatos, numero, estado, cidade, cod_cidade):
    id_nulo = []
    for i in numero:
        id_nulo.append("9")

    for candidato in candidatos:
        if candidato['numero'] == int(numero):
            #retorna_img_candidato_voto(candidato['id'], candidato['cod_cidade'])
            return candidato

    return {"id":"".join(id_nulo), "numero":"0", "nome": "nulo", "cod_cidade":cod_cidade, "estado": estado, "cidade": cidade, "partido": "nulo" }

def retorna_img_candidato_voto(id_candidato, cod_cidade):
    url_base = f"https://divulgacandcontas.tse.jus.br/divulga/rest/arquivo/img/2045202024/{id_candidato}/{cod_cidade}"
    response = requests.get(
        url=url_base,
        stream=True
    )
    if response.status_code == 200:
        with open(f"src/assets/{id_candidato}.jpg", 'wb') as f:
            f.write(response.content)

    print(response)

def get_votos_candidato(id_candidato, cod_cidade):
    cursor.execute("""SELECT votos FROM votacao WHERE id_candidato = ? and cod_cidade = ?""", (str(id_candidato), str(cod_cidade)))
    resultado_votos_candidato = cursor.fetchone()
    print(resultado_votos_candidato)
    if resultado_votos_candidato:
        return resultado_votos_candidato[0]
    else:
        return 0

def salva_voto_banco_dados(lista_candidatos):
    print("Salva voto")
    print(lista_candidatos)
    try:
        for candidato in lista_candidatos:
            votos = get_votos_candidato(candidato['id'], candidato['cod_cidade'])
            if votos == 0:
                cursor.execute(f"""INSERT INTO votacao (id_candidato, candidato, numero, votos, estado, cidade, cod_cidade) VALUES ("{candidato['id']}", "{candidato['nome']}", "{candidato['numero']}","1","{candidato['estado']}", "{candidato['cidade']}", "{candidato['cod_cidade']}") """)
                conexao.commit()
            else:
                cursor.execute(f"""UPDATE votacao SET votos = "{int(votos) + 1}" WHERE id_candidato = "{candidato['id']}" AND cod_cidade = "{candidato['cod_cidade']}" """)
                conexao.commit() 
        print("Eleitor votante salvo com sucesso!")
    except Exception as err:
        print("Não foi possivel salvar o voto! ", err)

def retorna_candidatos_backoffice(cidade, voto):
    lista_candidatos = []
    url_base = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/2024/{cidade}/2045202024/{voto}/candidatos"
    print(url_base)
    response = requests.get(
        url=url_base
    )

    for candidato in response.json()["candidatos"]:
        lista_candidatos.append({"id":candidato['id'] ,"numero":candidato['numero'], "nomeUrna":candidato["nomeUrna"], "descricaoTotalizacao": candidato["descricaoTotalizacao"], "nomeCompleto": candidato["nomeCompleto"],  "partido":candidato['partido']['sigla']})

    return lista_candidatos

def retorna_nome_cidade_por_codigo(cod_cidade):
    url_base = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/2024/{cod_cidade}/2045202024/13/candidatos"
    response = requests.get(
        url=url_base
    )
    return response.json()["unidadeEleitoral"]["nome"]


