import requests
import pandas as pd
import sqlite3
import datetime
import time


db_name = "monitoramento.db"
tb_name = "valor_bitcoin"


def get_value_bit():
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    ).json()

    return response["bitcoin"]["usd"]


def get_dateAndTime():
    today = str(datetime.datetime.now())
    today = today.split()
    today[1] = today[1].split(".")[0]
    return today


def inicia_banco(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS valor_bitcoin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dia TEXT NOT NULL,
        hora TEXT NOT NULL,
        valor_bit FLOAT
        )
        """
    )
    conn.close()


def atualiza_banco(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    data_hoje, hora_agora = get_dateAndTime()
    valor_agora = get_value_bit()
    cursor.execute(
        """
        INSERT INTO valor_bitcoin (dia, hora, valor_bit) VALUES (?,?,?)
        """,
        (data_hoje, hora_agora, valor_agora),
    )
    conn.commit()
    conn.close()


def ler_db(db_name, tb_name):
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query(f"SELECT * FROM {tb_name}", conn)
    print(df.to_string(index=False))
    conn.close()


inicia_banco(db_name)
print("Banco iniciado")
try:
    while True:
        atualiza_banco(db_name)
        print("Atualização feita, aguardando a proxima! (60s)")
        print("ctrl + c para encerrar")
        time.sleep(60)

except KeyboardInterrupt:
    print("Monitoramento interrompido!")

finally:
    print("Resumo")
    ler_db(db_name, tb_name)
