import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cria o navegador e salva o login em cache
dir_path = os.getcwd()
profile = os.path.join(dir_path, "profile", "wpp")
options = webdriver.ChromeOptions()
options.add_argument(
    r"user-data-dir={}".format(profile))

# Carregar informações do arquivo JSON
with open('dados.json') as json_file:
    dados_json = json.load(json_file)

# Extraindo informações da tarefa
msg = dados_json.get('mensagem')
numeros = dados_json.get('contatos')


def wpp_browser():
    # Define o diretório do perfil
    profile_directory = os.getcwd()  # Escolha o nome do diretório onde o cache será armazenado

    # Verifica se o diretório do perfil existe, se não, o cria
    if not os.path.exists(profile_directory):
        os.makedirs(profile_directory)

    # Cria o navegador e salva o login em cache
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir={}".format(os.path.abspath(profile_directory)))

    # Inicializar o navegador
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()

    # URL do WhatsApp Web
    whatsapp_url = "https://web.whatsapp.com/"
    browser.get(whatsapp_url)

    # Verifica se a página está carregada pela primeira vez
    first_load = True
    time.sleep(15)
    # Verifica se o QR code está presente somente na primeira carga da página
    while first_load:

        # Verifica se o QR code está presente
        if len(browser.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas')) < 1:
            print("QR code não encontrado. Continuando sem autenticação.")
            break  # Se o QR code não estiver presente, sai do loop

        # Se o QR code estiver presente, espera até que o painel lateral seja carregado
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, 'side')))
        first_load = False

    return browser


# Processo Span
def enviar_mensagem(browser, numeros, msg):
    # Enviar mensagem para cada contato na lista 'numeros'
    for numero in numeros:
        # Enviar mensagem para o contato
        search_box = browser.find_element(By.XPATH, "//div[@contenteditable='true']")
        search_box.send_keys(numero, Keys.ENTER)
        time.sleep(0.5)  # Aguarde para garantir que o contato seja carregado
        # Digitar a mensagem
        message_box = browser.find_element(By.XPATH, "//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p")
        message_box.send_keys(msg, Keys.ENTER)


''' # Enviando cada parágrafo da mensagem
    for message in mensagem:
        message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='1']")
        message_box.send_keys(message)
        message_box.send_keys(Keys.SHIFT, Keys.ENTER)

    message_box.send_keys(Keys.ENTER)'''

# Chamar a função para configurar o navegador com o cache do WhatsApp Web
browser = wpp_browser()
time.sleep(15)
enviar_mensagem(browser, numeros, msg)


