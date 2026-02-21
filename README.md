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
![python-api-pandas-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/11084ed5-4701-481e-a013-b6fc8342029f)


<img width="419" height="191" alt="image" src="https://github.com/user-attachments/assets/86d6b84e-c822-46ff-971f-17ced0973467" />

## 🚀 Como Rodar
 
# Clone o repositório
git clone https://github.com/ovictoraffonso/monitor_crypto.git

# Instale as dependências
pip install requests pandas matplotlib

# Execute o monitoramento
python monitor_crypto/monitor.py
