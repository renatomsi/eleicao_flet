from src.services.database import ELEITORES
import sqlite3
import requests
import json

conexao = sqlite3.connect("desenvolvimento2.db", check_same_thread=False)
cursor = conexao.cursor()


def create_banco_dados():
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS eleitores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            estado TEXT NOT NULL,
            cidade TEXT NOT NULL,
            titulo_eleitor TEXT NOT NULL
        )              
        """)

        cursor.execute("""
        CREATE TABLE "eleitores_votantes" (
            "titulo_eleitor"	TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE "votacao" (
            "id_candidato"	TEXT NOT NULL,
            "candidato"	TEXT NOT NULL,
            "numero"	TEXT NOT NULL,
            "votos"	TEXT NOT NULL,
            "estado"	TEXT NOT NULL,
            "cidade"	TEXT NOT NULL
        , "cod_cidade"	TEXT NOT NULL)
        """)

        for eleitor in ELEITORES:
            nome = eleitor["nome"]
            estado = eleitor["estado"]
            cidade = eleitor["cidade"]
            titulo_eleitor = eleitor["titulo_eleitor"]
            print(f"{nome}, {estado}, {cidade}, {titulo_eleitor}")

            cursor.execute(f"""
            INSERT INTO eleitores (nome, estado, cidade, titulo_eleitor) VALUES ("{nome}"," {estado}", "{cidade}", "{titulo_eleitor}")
            """)

        conexao.commit()
        conexao.close()

    except Exception as err:
        print("Não foi possivel Criar banco de dados!\n", err)