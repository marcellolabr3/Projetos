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


def draw():
            screenshot = pyautogui.screenshot()
            screenshot_cv = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
            cv2.imwrite('screenshot_temp.png', screenshot_cv)
            screenshot = cv2.imread('screenshot_temp.png')
            caminho_QR5 = '768.png'
            template = cv2.imread(caminho_QR5)
            resultado = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            locations = np.where(resultado >= threshold)
             
            if locations[0].any():
                y, x = locations[0][0], locations[1][0]
                pyautogui.click(x=x, y=y)
                time.sleep(0.3)            
           # pyautogui.press('d')
                pyautogui.press('b')
            # pyautogui.press('alt')
            # pyautogui.press('d')
            # pyautogui.press('b')
                time.sleep(0.3)
            
                screenshot = pyautogui.screenshot()
                screenshot_cv = np.array(screenshot)
                screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
                cv2.imwrite('screenshot_temp.png', screenshot_cv)
                screenshot = cv2.imread('screenshot_temp.png')
                caminho_arquivo = 'arquivo.png'        
                template = cv2.imread(caminho_arquivo)
                resultado = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.6
                locations = np.where(resultado >= threshold)
             
                if locations[0].any():
                    y, x = locations[0][0], locations[1][0]
                # Calcula a nova posição descendo 1cm
                    nova_posicao_y = y + 60  # Supondo que 1cm tenha 30 pixels
                    pyautogui.doubleClick(x=x, y=nova_posicao_y)
        
                
draw()