import requests
import pandas as pd
import sqlite3
import datetime
import matplotlib.pyplot as plt


df_name = "monitoramento.db"
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
    return today  # [dia][hora]


def inicia_banco(df_name):
    conn = sqlite3.connect(df_name)
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


def atualiza_banco(df_name):
    conn = sqlite3.connect(df_name)
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
    return hora_agora, valor_agora


def to_csv(df_name, tb_name):
    conn = sqlite3.connect(df_name)
    df = pd.read_sql_query(f"SELECT * FROM {tb_name}", conn)
    df = df.to_csv("monitoramento.csv", index=False)
    conn.close()


def mostra_grafico(x, y):
    plt.clf()
    plt.plot(x, y)
    plt.title("Variação do bitcoin")
    plt.ylabel("Valor em dolar")
    plt.xlabel("Hora")


inicia_banco(df_name)
print("Banco iniciado")

try:
    contagem = 1
    x = []
    y = []
    plt.ion()
    mostra_grafico(x, y)
    while plt.get_fignums():
        cords_x, cords_y = atualiza_banco(df_name)
        print(f"{contagem}° atualização feita, aguardando a proxima! (20s)")

        x.append(cords_x)
        y.append(cords_y)

        mostra_grafico(x, y)

        plt.pause(20)

        contagem += 1
except KeyboardInterrupt:
    print("Monitoramento interrompido!")

except Exception:
    print("Erro de requisição")

finally:
    to_csv(df_name, tb_name)
    print("Dados obtidos em .csv")
