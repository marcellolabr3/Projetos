import time
import json
import csv
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def carregar_dados_json():
    # Carregar informações do arquivo JSON
    with open('dados.json', encoding='utf-8') as json_file:
        dados_json = json.load(json_file)
        return dados_json.get('mensagem'), dados_json.get('contatos')


def wpp_browser():
    # Define o diretório do perfil
    profile_directory = os.getcwd()

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
    time.sleep(10)
    # Verifica se o QR code está presente somente na primeira carga da página
    while first_load:
        try:
            # Verifica se o QR code está presente
            qr_code_elements = browser.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas')
            if len(qr_code_elements) < 1:
                print("QR code não encontrado. Continuando sem autenticação.")
                break  # Se o QR code não estiver presente, sai do loop

            # Se o QR code estiver presente, espera até que o painel lateral seja carregado
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, 'side')))
            first_load = False
        except Exception as e:
            print("Erro ao carregar o WhatsApp Web:", e)

    return browser


def enviar_mensagem(browser, mensagem, contatos):
    enviados = []  # Lista para armazenar os números para os quais a mensagem foi enviada

    # Enviar mensagem para cada contato na lista 'contatos'
    for contato in contatos:
        try:
            # Enviar mensagem para o contato
            search_box = browser.find_element(By.XPATH, "//div[@contenteditable='true']")
            search_box.send_keys(contato, Keys.ENTER)
            time.sleep(0.5)  # Aguarde para garantir que o contato seja carregado
            # Digitar a mensagem
            message_box = browser.find_element(By.XPATH,
                                               "//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p")
            message_box.send_keys(mensagem, Keys.ENTER)

            # Salvar o número para o qual a mensagem foi enviada
            enviados.append(contato)
        except Exception as e:
            print("Erro ao enviar mensagem para o contato", contato, ":", e)

    return enviados


def salvar_enviados(enviados):
    # Salvar os números para os quais a mensagem foi enviada em um arquivo CSV
    with open('enviados.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Mensagem enviada para'])
        writer.writerows([[numero] for numero in enviados])


def exibir_janela_numeros_enviados(enviados):
    # Exibir uma janela com a quantidade de números para os quais a mensagem foi enviada
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    messagebox.showinfo("Mensagens Enviadas", "Foram enviadas mensagens para {} números.".format(len(enviados)))


def main():
    # Carregar informações do arquivo JSON
    mensagem, contatos = carregar_dados_json()

    # Chamar a função para configurar o navegador com o cache do WhatsApp Web
    browser = wpp_browser()

    # Enviar mensagens e obter os números para os quais a mensagem foi enviada
    enviados = enviar_mensagem(browser, mensagem, contatos)

    # Salvar os números enviados em um arquivo CSV
    salvar_enviados(enviados)

    # Exibir a quantidade de números para os quais a mensagem foi enviada em uma janela
    exibir_janela_numeros_enviados(enviados)

    # Fechar o navegador
    browser.quit()


if __name__ == "__main__":
    main()
