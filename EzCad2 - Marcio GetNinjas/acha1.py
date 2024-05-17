import shutil
import sys
import tkinter as tk
from tkinter import messagebox
import pyautogui
import keyboard
import os
import subprocess
import time
import cv2
import numpy as np
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
import pystray
from pystray import MenuItem as item
from PIL import Image

import time

# def ver_img():
#     nomes_arquivos = ['marking1360.png', 'marking1920.png']
#     while True:
#         screenshot = pyautogui.screenshot()
#         screenshot_cv = np.array(screenshot)
#         screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
#         cv2.imwrite('screenshot_temp.png', screenshot_cv)
#         screenshot = cv2.imread('screenshot_temp.png')
#
#         for caminho_arquivo in nomes_arquivos:
#             print(f"Lendo o arquivo: {caminho_arquivo}")
#             template = cv2.imread(caminho_arquivo)
#
#             if template is not None:
#                 print(f"Arquivo {caminho_arquivo} carregado com sucesso.")
#
#                 resultado = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
#                 threshold = 0.7
#                 locations = np.where(resultado >= threshold)
#
#                 if locations[0].any():
#                     print(f"Correspondência encontrada para o arquivo: {caminho_arquivo}")
#                     y, x = locations[0][0], locations[1][0]
#                     tamanho_horizontal, tamanho_vertical = pyautogui.size()
#                     novo_x = min(x + 255, tamanho_horizontal - 200)
#                     novo_y = min(y + 150, tamanho_vertical - 0)
#                     pyautogui.moveTo(x=novo_x, y=novo_y)
#                     pyautogui.click()
#                     return False
#                 else:
#                     print('nao achei')
#         time.sleep(1)  # Pausa por 1 segundo antes de verificar novamente
#
# #
# # def ver_OK():
# #     if botaOK == 'OK':
# #         print("OK pressionado.")
# #         pyautogui.hotkey("f2")
# #         self.encontrando_tarja()  # Chama a função para encontrar a tarja
# #         return False
# #     else:
# #         print("Botão OK não foi pressionado.")
#
# ver_img()  # Chama a função para iniciar o monitoramento
#

# def encontrand_ok():
#     press_Ok = 'press_Ok.png'
#     template = cv2.imread(press_Ok, cv2.IMREAD_GRAYSCALE)
#     threshold = 0.9
#
#     while True:
#         screenshot = pyautogui.screenshot()
#         screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
#         gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
#         result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
#         locations = np.where(result >= threshold)
#
#         if locations[0].any():
#             print('achou')
#             break
#
#     while True:
#         screenshot = pyautogui.screenshot()
#         screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
#         gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
#         result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
#         locations = np.where(result >= threshold)
#
#         if not locations[0].any():
#             print('apertar o f2 e chamar encontrando tarja')
#             # pyautogui.hotkey("f2")
#             # self.encontrando_tarja()  # Chama a função para encontrar a tarja
#             break
#
#     return False
#
#
#
#
#     time.sleep(0.5)
#
#
#
# encontrand_ok()



import threading
import pyautogui
import cv2
import numpy as np

# Função para monitorar a tela em uma thread separada
def monitorar_tela():
    # Loop infinito para monitorar a tela
    nomes_arquivos = ['marking1360.png', 'marking1920.png']
    while True:
        screenshot = pyautogui.screenshot()
        screenshot_cv = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
        cv2.imwrite('screenshot_temp.png', screenshot_cv)
        screenshot = cv2.imread('screenshot_temp.png')

        for caminho_arquivo in nomes_arquivos:
            print(f"Lendo o arquivo: {caminho_arquivo}")
            template = cv2.imread(caminho_arquivo)

            if template is not None:
                print(f"Arquivo {caminho_arquivo} carregado com sucesso.")

                resultado = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.7
                locations = np.where(resultado >= threshold)

                if locations[0].any():
                    print(f"Correspondência encontrada para o arquivo: {caminho_arquivo}")
                    y, x = locations[0][0], locations[1][0]
                    tamanho_horizontal, tamanho_vertical = pyautogui.size()
                    novo_x = min(x + 255, tamanho_horizontal - 200)
                    novo_y = min(y + 150, tamanho_vertical - 0)
                    pyautogui.moveTo(x=novo_x, y=novo_y)
                    pyautogui.click()
                    return False
                else:
                    print('nao achei')
        time.sleep(1)  # Pausa por 1 segundo antes de verificar novamente

# Função para exibir a caixa de diálogo e iniciar a thread
def exibir_alerta():
    pyautogui.alert(text='Pressione OK para continuar...', title='Aguardando continuar')


# Cria e inicia a thread para monitorar a tela
monitor_thread = threading.Thread(target=monitorar_tela)
monitor_thread.start()

# Exibe a caixa de diálogo para o usuário

exibir_alerta()
