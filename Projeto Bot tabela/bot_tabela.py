import time
import json
import csv
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tkinter import messagebox
import time
import os
import sys
import threading
from datetime import datetime
import certifi



# # Definir a data e hora limite
# data_limite = datetime(2030, 5, 1, 18, 0)
#
#
# def calcular_tempo_restante():  # Calcular o tempo restante até a data limite
#     tempo_restante = data_limite - datetime.now()
#     dias = tempo_restante.days
#     horas, segundos = divmod(tempo_restante.seconds, 3600)
#     minutos = segundos // 60
#     return f"Tempo restante: {dias} dias, {horas} horas e {minutos} minutos."
#
#
# # Verificar se a hora atual está além do limite permitido
# def verificar_limite_tempo():
#     hora_atual = datetime.now()
#     return hora_atual > data_limite
#
#
# # Verificar se a hora limite já passou
# def verificar_hora_limite():
#     return verificar_limite_tempo()
#
#
# # Criar um loop que verifica a hora atual e encerra o programa se a hora limite passou
# def verificar_hora_loop():
#     while not verificar_hora_limite():
#         time.sleep(60)  # Verificar a cada minuto
#     messagebox.showinfo("Prazo Expirado", "O prazo para utilizar o software expirou.")
#     sys.exit()  # Encerrar o programa
#
#
# # Iniciar a verificação contínua da hora limite em uma thread separada
# hora_thread = threading.Thread(target=verificar_hora_loop)
# hora_thread.start()
#
#
# # Verificar a hora limite antes de abrir a interface
# if verificar_hora_limite():
#     messagebox.showinfo("Prazo Expirado", "O prazo para utilizar o software expirou.")
#     sys.exit()  # Encerrar o programa
#
#
# # Definir a mensagem a ser exibida no programa DEMO
# mensagem = (f"Este é um programa DEMO e estará disponível até as {data_limite.strftime('%H:%M')} do dia "
#             f"{data_limite.strftime('%d/%m/%Y')}.\n\n")
# mensagem += calcular_tempo_restante()
# messagebox.showinfo("Aviso", mensagem)



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

    # Define um tempo de espera máximo
    max_wait_time = 60  # 60 segundos

    # Verifica se a página está carregada pela primeira vez
    first_load = True

    # Verifica se o QR code está presente somente na primeira carga da página
    while first_load:
        try:
            # Verifica se o QR code está presente
            qr_code_elements = browser.find_elements(By.XPATH,
                                                     '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas')
            if len(qr_code_elements) < 1:
                print("QR code não encontrado. Continuando sem autenticação.")
                break  # Se o QR code não estiver presente, sai do loop

            # Se o QR code estiver presente, espera até que o painel lateral seja carregado
            WebDriverWait(browser, max_wait_time).until(EC.presence_of_element_located((By.ID, 'side')))
            first_load = False
        except TimeoutException:
            # Se o tempo de espera máximo for atingido, sai do loop
            print("Tempo máximo de espera excedido. Continuando sem autenticação.")
            break
        except Exception as e:
            print("Erro ao carregar o WhatsApp Web:", e)

    # Se não for a primeira carga, espera até que o painel lateral seja carregado
    if not first_load:
        try:
            WebDriverWait(browser, max_wait_time).until(EC.presence_of_element_located((By.ID, 'side')))
        except TimeoutException:
            print("Tempo máximo de espera excedido. Continuando sem autenticação.")
        except Exception as e:
            print("Erro ao carregar o WhatsApp Web:", e)

    return browser


# Função para enviar uma mensagem
def enviar_mensagem(browser, mensagem, contatos, max_wait_time):
    enviados = []  # Inicializa a lista fora do bloco try

    try:
        # Espera até que o painel lateral esteja presente
        WebDriverWait(browser, max_wait_time).until(EC.presence_of_element_located((By.ID, 'side')))

        # Enviar mensagem para cada contato na lista 'contatos'
        for contato in contatos:
            try:
                # Espera até que o campo de busca de contatos esteja presente
                WebDriverWait(browser, max_wait_time).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']")))

                # Enviar mensagem para o contato
                search_box = browser.find_element(By.XPATH, "//div[@contenteditable='true']")
                search_box.send_keys(contato, Keys.ENTER)

                time.sleep(0.5)  # Aguarde para garantir que o contato seja carregado

                # Espera até que o campo de digitação de mensagem esteja presente
                WebDriverWait(browser, max_wait_time).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p")))

                # Digitar a mensagem
                message_box = browser.find_element(By.XPATH,
                                                   "//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p")
                message_box.send_keys(mensagem, Keys.ENTER)

                # Salvar o número para o qual a mensagem foi enviada
                enviados.append(contato)
            except Exception as e:
                print("Erro ao enviar mensagem para o contato", contato, ":", e)
    except TimeoutException:
        print("Tempo máximo de espera excedido ao carregar o painel lateral.")

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
    enviados = enviar_mensagem(browser, mensagem, contatos, 60)

    # Salvar os números enviados em um arquivo CSV
    salvar_enviados(enviados)

    # Exibir a quantidade de números para os quais a mensagem foi enviada em uma janela
    exibir_janela_numeros_enviados(enviados)


if __name__ == "__main__":
    main()
