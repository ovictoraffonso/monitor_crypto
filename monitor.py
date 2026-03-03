import requests
import pandas as pd
import sqlite3
import datetime
import matplotlib.pyplot as plt


df_name = "monitoramento.db"
tb_name = "valor_bitcoin"


def get_value_bit():
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        ).json()

        return response["bitcoin"]["usd"]

    except Exception:
        print("Erro de requisição!")
        return None


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
    data_hoje, hora_agora = get_dateAndTime()
    valor_agora = get_value_bit()
    if valor_agora is not None:
        try:
            conn = sqlite3.connect(df_name)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO valor_bitcoin (dia, hora, valor_bit) VALUES (?,?,?)
                """,
                (data_hoje, hora_agora, valor_agora),
            )
            conn.commit()
            conn.close()
        except Exception:
            raise Exception("Erro na atualização")

    return hora_agora, valor_agora


def to_csv(df_name, tb_name):
    conn = sqlite3.connect(df_name)
    query = f"""SELECT  id, 
                    dia, 
                    hora, 
                    valor_bit, 
                    valor_bit - (lag(valor_bit) OVER (ORDER BY id)) AS diferenca 
                    FROM {tb_name}
                """
    df = pd.read_sql_query(query, conn)
    df.to_csv("monitoramento.csv", index=False)
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

        if cords_y is not None:
            print(f"{contagem}° atualização feita, aguardando a proxima! (20s)")
            contagem += 1

            x.append(cords_x)
            y.append(cords_y)

            mostra_grafico(x, y)

        plt.pause(20)

except KeyboardInterrupt:
    print("Monitoramento interrompido!")

except Exception:
    print("Erro de requisição")

finally:
    to_csv(df_name, tb_name)
    print("Dados obtidos em .csv")
