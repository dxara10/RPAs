import tkinter as tk
import pandas as pd
import sqlite3
import datetime as dt
import time as tm
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime

# Conexão com o banco de dados SQLite
conexao = sqlite3.connect('Banco_CHAMADAS.db')
c = conexao.cursor()

# Criação da tabela CHAMADAS
c.execute('''
CREATE TABLE IF NOT EXISTS CHAMADAS (
    ALVO text,
    TERMINAL int,
    TELINTERLOCUTOR int,
    INTERLOCUTORES text,
    AUDIO varchar(255),
    MENSAGEM varchar(255),
    HTML varchar(255),
    DATA date,
    HORAINICIAL time,
    HORAFINAL time,
    DURACAO time
)
''')
conexao.commit()
conexao.close()

# Definição do diretório de chamadas
diretorio = r"C:\Users\PC\Desktop\CLIENTE\CHAMADAS"

# Processo de raspagem dos arquivos HTML no diretório
for arquivo in os.listdir(diretorio):
    if arquivo.endswith(".html"):
        caminho = os.path.join(diretorio, arquivo)

        # Configuração do navegador em modo headless
        chrome_options = Options()
        chrome_options.headless = True
        navegador = webdriver.Chrome(options=chrome_options)
        navegador.get("file:///" + caminho)

        # Extração de dados do arquivo HTML
        ALVO = navegador.find_element(By.XPATH, '/html/body/center/table[2]/caption').get_attribute("textContent")

        TERMINAL = navegador.find_element(By.XPATH, '/html/body/center/table[1]/tbody/tr[2]/td[1]').get_attribute("textContent")
        TERMINAL = TERMINAL[3:5] + TERMINAL[6:14]

        TELINTERLOCUTOR = navegador.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[4]').get_attribute("textContent")

        interlocutores = navegador.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[4]').get_attribute("textContent")
        INTERLOCUTORES = interlocutores + "/" + TERMINAL

        AUDIO = navegador.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[9]').get_attribute("textContent")
        AUDIO = "C:\\Users\\PC\\Desktop\\CLIENTE\\Gravacoes\\Gravacoes\\" + AUDIO[0:8] + '.wav'

        MENSAGEM = navegador.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td').get_attribute("textContent")

        HTML = navegador.find_element(By.XPATH, '/html').get_attribute("baseURI")

        DATA = navegador.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[5]').get_attribute("textContent")[0:10]

        horainicial = navegador.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[5]').get_attribute("textContent")[11:19]
        tempo1_delta = datetime.strptime(horainicial, '%H:%M:%S') - datetime.strptime('00:00:00', '%H:%M:%S')
        HORAINICIAL = tempo1_delta

        duracao = navegador.find_element(By.XPATH, '/html/body/center/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[6]').get_attribute("textContent")
        tempo2_delta = datetime.strptime(duracao, '%H:%M:%S') - datetime.strptime('00:00:00', '%H:%M:%S')
        DURAÇAO = tempo2_delta

        tempo_soma = tempo1_delta + tempo2_delta
        HORAFINAL = str(tempo_soma)[-8:]

        navegador.quit()

        # Inserção dos dados no banco de dados SQLite
        conexao = sqlite3.connect('Banco_CHAMADAS.db')
        c = conexao.cursor()
        c.execute('''
            INSERT INTO CHAMADAS (
                ALVO, TERMINAL, TELINTERLOCUTOR, INTERLOCUTORES, AUDIO, MENSAGEM, HTML, DATA, HORAINICIAL, HORAFINAL, DURACAO
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ALVO, TERMINAL, TELINTERLOCUTOR, INTERLOCUTORES, AUDIO, MENSAGEM, HTML, DATA, HORAINICIAL, HORAFINAL, DURAÇAO))

        conexao.commit()
        conexao.close()

# Exportação dos registros do banco para um arquivo Excel
conexao = sqlite3.connect('Banco_CHAMADAS.db')
c = conexao.cursor()
c.execute("SELECT *, oid FROM CHAMADAS")
registros_exportados = c.fetchall()
registros_exportados = pd.DataFrame(registros_exportados, columns=[
    'ALVO', 'TERMINAL', 'TELINTERLOCUTOR', 'INTERLOCUTORES', 'AUDIO', 'MENSAGEM', 'HTML', 'DATA', 'HORAINICIAL', 'HORAFINAL', 'DURAÇAO', 'Id_banco'
])
registros_exportados.to_excel('CHAMADAS.xlsx')
conexao.commit()
conexao.close()
