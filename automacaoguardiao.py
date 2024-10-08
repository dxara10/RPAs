
import tkinter as tk
import pandas as pd
import sqlite3

conexao = sqlite3.connect('Banco_CHAMADAS.db')
c = conexao.cursor()
c.execute(''' CREATE TABLE CHAMADAS (
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
    DURAÇÃO time)
    ''')
conexao.commit()
conexao.close()


#PROCESSODE RASPAGEM EM SI

import datetime as dt
import time as tm
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sqlite3

#ATENÇÃO: no próprio computador do Antônio eu fiz algumas alterações no código para este interagir com o usuário, exemplo aqui no diretório, eu chamei a função input(“perguntando a pasta a ser compilada”), atribuindo a mesma à variável diretorio
diretorio = r"C:\Users\PC\Desktop\ANTÔNIO\CHAMADAS"        


for arquivo in os.listdir(diretorio):
    if arquivo.endswith(".html"):
        caminho = os.path.join(diretorio, arquivo)
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.headless = True 
        navegador = webdriver.Chrome(options=chrome_options)
        navegador.get("file:///" + caminho)
        
        ALVO = navegador.find_element(By.XPATH,
            '/html/body/center/table[2]/caption').get_attribute("textContent")

        TERMINAL = navegador.find_element(By.XPATH,
            '/html/body/center/table[1]/tbody/tr[2]/td[1]').get_attribute("textContent")
        t1 = TERMINAL[3:5] + TERMINAL[6:14]
        TERMINAL = t1

        TELINTERLOCUTOR = navegador.find_element(By.XPATH,
            '/html/body/center/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[4]').get_attribute("textContent")

        interlocutores = navegador.find_element(By.XPATH,
            '/html/body/center/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[4]').get_attribute("textContent")
        INTERLOCUTORES = interlocutores + "/" + TERMINAL

        #adaptar
        AUDIO = navegador.find_element(By.XPATH,
            '/html/body/center/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[9]').get_attribute("textContent")
        a2 = "C:\\Users\\PC\\Desktop\\ANTÔNIO\\Gravacoes\\Gravacoes\\"
        a3 = '.wav'
        a1 = a2 + AUDIO[0:8] + a3
        AUDIO = a1
        
        
        MENSAGEM = navegador.find_element(By.XPATH,
            '/html/body/center/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td').get_attribute("textContent")
        
            
        HTML = navegador.find_element(By.XPATH,
            '/html').get_attribute("baseURI")
        
        DATA = navegador.find_element(By.XPATH,
            '/html/body/center/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[5]').get_attribute("textContent")
        d1 = DATA[0:10]
        DATA = d1
        
        horainicial = navegador.find_element(By.XPATH,
            '/html/body/center/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[5]').get_attribute("textContent")
        h1 = horainicial[11:19]
        horainicial = h1
        tempo1_delta = datetime.strptime(horainicial, '%H:%M:%S') - datetime.strptime('00:00:00', '%H:%M:%S')
        HORAINICIAL = tempo1_delta
        
        duração = navegador.find_element(By.XPATH,
            '/html/body/center/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[6]').get_attribute("textContent")
        tempo2_delta = datetime.strptime(duração, '%H:%M:%S') - datetime.strptime('00:00:00', '%H:%M:%S')
        DURAÇÃO = tempo2_delta
        
        tempo_soma = tempo1_delta + tempo2_delta
        tempo_soma_str = str(tempo_soma)
        tempo_soma_str = tempo_soma_str[-8:]
        HORAFINAL = tempo_soma_str
        
        
        
        navegador.quit()
        
        
        
        
        conexao = sqlite3.connect('Banco_CHAMADAS.db')
        c = conexao.cursor()
        c.execute(" INSERT INTO CHAMADAS VALUES (:ALVO, :TERMINAL, :TELINTERLOCUTORES, :INTERLOCUTORES, :AUDIO, :MENSAGEM, :HTML, :DATA, :HORAINICIAL, :HORAFINAL, :DURAÇÃO)",
                     {
                         'ALVO':ALVO,
                 
                         'TERMINAL':TERMINAL,
                 
                         'TELINTERLOCUTORES':TELINTERLOCUTOR,
                         
                         'INTERLOCUTORES':INTERLOCUTORES,
                         
                         'AUDIO':AUDIO,
                         
                         'MENSAGEM':MENSAGEM,
                         
                         'HTML':HTML,
                         
                         'DATA':DATA,
                 
                         'HORAINICIAL':horainicial,
                         
                         'HORAFINAL':tempo_soma_str,
                        
                         'DURAÇÃO':duração
                         
                     })
            
        conexao.commit()
        conexao.close()

#EXPORTAÇÃO TABELA, a tabela aparece na mesma pasta onde o programa é executado, atenção aos nomes dados como está abaixo, “CHAMADAS.XLSX”

conexao = sqlite3.connect('Banco_CHAMADAS.db')
c = conexao.cursor()
c.execute("SELECT *, oid FROM CHAMADAS")
registros_exportados = c.fetchall()
registros_exportados = pd.DataFrame(registros_exportados, columns=['ALVO','TERMINAL','TELINTERLOCUTORES','INTERLOCUTORES','AUDIO','MENSAGEM','HTML','DATA','HORAINICIAL','HORAFINAL','DURAÇÃO','Id_banco'])
registros_exportados.to_excel('CHAMADAS.xlsx')
conexao.commit()
conexao.close()





