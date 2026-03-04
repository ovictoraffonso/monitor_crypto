import requests
import pandas as pd
import sqlite3
import datetime
import matplotlib.pyplot as plt


df_name = "monitoramento.db"
tb_name = "valor_bitcoin"
contagem = 1


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
    with sqlite3.connect(df_name) as conn:
        cursor = conn.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS valor_bitcoin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dia TEXT NOT NULL,
            hora TEXT NOT NULL,
            valor_bit FLOAT
            )
            """
        cursor.execute(query)


def atualiza_banco(df_name):
    data_hoje, hora_agora = get_dateAndTime()
    valor_agora = get_value_bit()
    if valor_agora is not None:
        try:
            with sqlite3.connect(df_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO valor_bitcoin (dia, hora, valor_bit) VALUES (?,?,?)
                    """,
                    (data_hoje, hora_agora, valor_agora),
                )
                conn.commit()
        except Exception:
            raise Exception("Erro na atualização")

    return hora_agora, valor_agora


def to_csv(df_name):
    df = data_Formatado(df_name)
    df.to_csv("monitoramento.csv", index=False)


def mostra_grafico(df_name):
    df = data_Formatado(df_name)
    plt.clf()
    plt.plot(df["hora"], df["valor_bit"], marker="o", label="Valor em dolar")
    plt.plot(df["hora"], df["media_movel"], label="Média movel")
    plt.grid(True)
    plt.title("Variação bitcoin")
    plt.ylabel("Valor bitcoin")
    plt.xlabel("hora")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()


def data_Formatado(df_name):
    with sqlite3.connect(df_name) as conn:
        df = pd.read_sql("SELECT * FROM valor_bitcoin", conn)

    df["diferenca"] = df["valor_bit"].diff()
    df["media_movel"] = round(
        df["valor_bit"].rolling(window=3, min_periods=1).mean(), 3
    )
    return df


inicia_banco(df_name)
print("Banco iniciado")

try:
    plt.ion()
    mostra_grafico(df_name)

    while plt.get_fignums():
        hora, valor = atualiza_banco(df_name)

        if valor is not None:
            print(f"{contagem}° atualização feita, aguardando a proxima! (20s)")
            contagem += 1

            mostra_grafico(df_name)
            plt.draw()

        plt.pause(20)

except KeyboardInterrupt:
    print("Monitoramento interrompido!")

except Exception:
    print("Erro desconhecido")

finally:
    to_csv(df_name)
    print("Dados obtidos em .csv")
