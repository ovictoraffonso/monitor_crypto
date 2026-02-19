# Monitor de Cotação BTC

> Um pipeline de ETL (Extract, Transform, Load) leve desenvolvido em Python para extração de dados em tempo real de APIs financeiras e armazenamento em banco de dados relacional

## 🛠️ Tecnologias Utilizadas

- **Python** (Linguagem Principal)
- **SQLite3** (Banco de Dados Relacional)
- **Pandas** (Análise e Manipulação de Dados)
- **Requests** (Consumo de API REST)

## ✨ Funcionalidades Principais
- **Coleta Automatizada:** Consumo contínuo da API pública da CoinGecko para monitoramento do valor do Bitcoin (USD).
- **Persistência de Dados: (Load)** Inserção e armazenamento seguro dos dados temporais em um banco local SQLite. 
- **Resiliência e Controle:** Implementação de pausas estratégicas (Rate Limiting) para respeitar os limites de requisição da API sem derrubar a aplicação.

## 🧠 Desafios Técnicos

O principal desafio foi criar um loop infinito de monitoramento sem causar travamentos (locks) no banco de dados SQLite. Isso foi resolvido isolando a abertura e o fechamento da conexão com o banco a cada ciclo de inserção. Além disso, foi necessário tratar as strings de data e hora geradas pela biblioteca datetime para manter o padrão correto no banco.

## 📸 Screenshots

![alt text](image-1.png)

## 🚀 Como Rodar
 
# Clone o repositório
git clone https://github.com/ovictoraffonso/monitor_crypto.git

# Instale as dependências
pip install requests pandas

# Execute o monitoramento
python monitor.py