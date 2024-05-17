def definicoes_ini():
    time.sleep(0.7)
    pyautogui.hotkey('ctrl', 'o')
    time.sleep(1)
    pyautogui.write('QR5.ezd')
    pyautogui.press('ENTER')
    time.sleep(0.5)

    screenshot = pyautogui.screenshot()
    screenshot_cv = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
    cv2.imwrite('screenshot_temp.png', screenshot_cv)
    screenshot = cv2.imread('screenshot_temp.png')
    caminho_draw = 'draw.png'
    template = cv2.imread(caminho_draw)
    resultado = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    locations = np.where(resultado >= threshold)
    os.remove('screenshot_temp.png')

    if locations[0].any():
        # Resolvendo o posivionamento
        tamanho_horizontal, tamanho_vertical = pyautogui.size()
        x, y = 0, 0

        if tamanho_horizontal <= 1360 and tamanho_vertical <= 768:
            novo_x = min(x + 90, tamanho_horizontal + 620)
            novo_y = min(y + 120, tamanho_vertical - 645)
            pyautogui.click(x=novo_x, y=novo_y)
            pyautogui.press('delete')
        else:
            novo_x = min(x + 110, tamanho_horizontal + 690)
            novo_y = min(y + 125, tamanho_vertical - 650)
            pyautogui.click(x=novo_x, y=novo_y)
            pyautogui.press('delete')






import os
import pyautogui
import numpy as np
import cv2
import time

#
#
#
# def definicoes_ini():
#     time.sleep(0.7)
#     pyautogui.hotkey('ctrl', 'o')
#     time.sleep(1)
#     pyautogui.write('QR5.ezd')
#     pyautogui.press('ENTER')
#     time.sleep(0.5)
#
#     # Resolvendo o posivionamento
#     screenshot = pyautogui.screenshot()
#     screenshot_cv = np.array(screenshot)
#     screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
#     cv2.imwrite('screenshot_temp.png', screenshot_cv)
#     screenshot = cv2.imread('screenshot_temp.png')
#
#     # Lista de nomes de arquivos a serem verificados
#     nomes_arquivos = ['768.png', '1080.png']
#
#     # Loop sobre cada nome de arquivo
#     for caminho_arquivo in nomes_arquivos:
#         print(f"Lendo o arquivo: {caminho_arquivo}")
#
#         # Carrega o arquivo
#         template = cv2.imread(caminho_arquivo)
#
#         # Verifica se o arquivo foi carregado com sucesso
#         if template is not None:
#             print(f"Arquivo {caminho_arquivo} carregado com sucesso.")
#
#             # Verifica se há correspondência do template na tela
#             resultado = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
#             threshold = 0.8
#             locations = np.where(resultado >= threshold)
#             time.sleep(0.5)
#             if locations[0].any():
#                 print(f"Correspondência encontrada para o arquivo: {caminho_arquivo}")
#                 y, x = locations[0][0], locations[1][0]
#                 # Calcula o centro da imagem
#                 centro_x = x + int(template.shape[1] / 2)
#                 centro_y = y + int(template.shape[0] / 2)
#                 pyautogui.click(centro_x, centro_y)
#                 pyautogui.press('delete')
#
#                 break
#
time.sleep(3)
definicoes_ini()
