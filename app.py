import requests
import time
import sqlite3
import logging

# Configuração de logging
logging.basicConfig(filename='site_test.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s\n')

def test_site_response_time(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()

        if response.status_code == 200:
            request_time = end_time - start_time
            logging.info(f"Site: {url} - Tempo de resposta: {request_time:.2f} segundos")
            return request_time
        else:
            logging.error(f"Erro ao acessar {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Erro ao acessar {url}: {str(e)}")
        return None

def create_table():
    conn = sqlite3.connect('site_logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS site_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, response_time REAL)''')
    conn.commit()
    conn.close()

def insert_log(url, response_time):
    conn = sqlite3.connect('site_logs.db')
    c = conn.cursor()
    c.execute("INSERT INTO site_logs (url, response_time) VALUES (?, ?)", (url, response_time))
    conn.commit()
    conn.close()

# Lista de sites para testar
sites = ["https://www.example.com", "https://www.google.com", "https://www.github.com"]

# Criar a tabela no banco de dados
create_table()

# Testar cada site e registrar no banco de dados
for site in sites:
    response_time = test_site_response_time(site)
    if response_time is not None:
        insert_log(site, response_time)

