from tkinter import *
from tkinter import messagebox
import pyautogui 
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.etree import ElementTree as ET
import subprocess
import time
import os
import cv2
import numpy as np
import sys
import threading
from datetime import datetime, timedelta


def XeY():
        screenshot = pyautogui.screenshot()
        screenshot_cv = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
        cv2.imwrite('screenshot_temp.png', screenshot_cv)
        screenshot = cv2.imread('screenshot_temp.png')
        caminho_xey = 'xey2.png'
        template = cv2.imread(caminho_xey)

        # Verificar se o arquivo XML existe antes de tentar ler
        if not os.path.exists('coordenadas.xml'):
            messagebox.showerror("Erro", "O arquivo 'coordenadas.xml' não existe!")
            return

        # Tentar ler o arquivo XML e extrair as coordenadas
        try:
            valores_xml = ET.parse('coordenadas.xml').getroot()
            posicao_x = int(valores_xml.find('posicao_x').text)
            posicao_y = int(valores_xml.find('posicao_y').text)
            tamanho_x = int(valores_xml.find('tamanho_x').text)
            tamanho_y = int(valores_xml.find('tamanho_y').text)
            definicao_x = int(valores_xml.find('definicao_x').text)
            definicao_y = int(valores_xml.find('definicao_y').text)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler o arquivo XML: {e}")
            return

        resultado = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        locations = np.where(resultado >= threshold)

        if locations[0].any():
            if locations[0].any():
                y, x = locations[0][0], locations[1][0]
                # Clica acima 2 campos no position X
                tamanho_horizontal, tamanho_vertical = pyautogui.size()
                novo_x = min(x + 25, tamanho_horizontal - 30)
                novo_y = min(y - 60, tamanho_vertical - 50)
                pyautogui.doubleClick(x=novo_x, y=novo_y)
                pyautogui.write(str(posicao_x)) 
                pyautogui.press('tab')
                pyautogui.write(str(posicao_y))
                pyautogui.press('tab')
                pyautogui.write(str(tamanho_x))
                pyautogui.press('tab')
                pyautogui.write(str(tamanho_y))

                # Clica na definition
                y, x = locations[0][0], locations[1][0]
                # pyautogui.click(x=x, y=y)
                tamanho_horizontal, tamanho_vertical = pyautogui.size()
                novo_x = min(x + 120, tamanho_horizontal - 50)
                novo_y = min(y + 98, tamanho_vertical - 50)
                pyautogui.doubleClick(x=novo_x, y=novo_y)
                pyautogui.write(str(definicao_x))
                time.sleep(0.3)
                tamanho_horizontal, tamanho_vertical = pyautogui.size()
                novo_x = min(x + 120, tamanho_horizontal - 50)
                novo_y = min(y + 118, tamanho_vertical - 50)
                pyautogui.doubleClick(x=novo_x, y=novo_y)
                pyautogui.write(str(definicao_y))
                time.sleep(0.3)

                pyautogui.hotkey('alt', 'a')
                time.sleep(0.5)
                

                return True

        return False

XeY()