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
# import threading
# from datetime import datetime

# # Definir a data e hora limite
# data_limite = datetime(2024, 4, 10, 22, 0)


# def calcular_tempo_restante():  # Calcular o tempo restante até a data limite
#     tempo_restante = data_limite - datetime.now()
#     dias = tempo_restante.days
#     horas, segundos = divmod(tempo_restante.seconds, 3600)
#     minutos = segundos // 60
#     return f"Tempo restante: {dias} dias, {horas} horas e {minutos} minutos."


# # Verificar se a hora atual está além do limite permitido
# def verificar_limite_tempo():
#     hora_atual = datetime.now()
#     return hora_atual > data_limite


# # Verificar se a hora limite já passou
# def verificar_hora_limite():
#     return verificar_limite_tempo()


# # Criar um loop que verifica a hora atual e encerra o programa se a hora limite passou
# def verificar_hora_loop():
#     while not verificar_hora_limite():
#         time.sleep(60)  # Verificar a cada minuto
#     messagebox.showinfo("Prazo Expirado", "O prazo para utilizar o software expirou.")
#     sys.exit()  # Encerrar o programa


# Iniciar a verificação contínua da hora limite em uma thread separada
# hora_thread = threading.Thread(target=verificar_hora_loop)
# hora_thread.start()


# # Verificar a hora limite antes de abrir a interface
# if verificar_hora_limite():
#     messagebox.showinfo("Prazo Expirado", "O prazo para utilizar o software expirou.")
#     sys.exit()  # Encerrar o programa


# # Definir a mensagem a ser exibida no programa DEMO
# mensagem = (f"Este é um programa DEMO e estará disponível até as {data_limite.strftime('%H:%M')} do dia "
#             f"{data_limite.strftime('%d/%m/%Y')}.\n\n")
# mensagem += calcular_tempo_restante()
# messagebox.showinfo("Aviso", mensagem)

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
cancelado = False


# Função principal que inicia o programa
def main():
    # Variável global para indicar se o botão "Cancelar" foi clicado
    global cancelado
    cancelado = False

    def cancelar():
        global cancelado
        cancelado = True
        janela.destroy()

    # Função para verificar se a pasta 'a_gravar' está vazia
    def verificar_pastas():
        pasta_a_gravar = "a_gravar"
        pasta_gravados = "gravados"

        # Verifica se as pastas existem, caso contrário, cria-as
        if not os.path.exists(pasta_a_gravar):
            os.makedirs(pasta_a_gravar)

        if not os.path.exists(pasta_gravados):
            os.makedirs(pasta_gravados)

        # Lista todos os arquivos na pasta 'a_gravar'
        arquivos_a_gravar = [arquivo.name for arquivo in os.scandir(pasta_a_gravar)]

        # Verifica se a pasta está vazia ou se contém apenas o arquivo 'QR5.ezd'
        if not arquivos_a_gravar or (len(arquivos_a_gravar) == 1 and arquivos_a_gravar[0] == "QR5.ezd"):
            messagebox.showinfo("Atenção",
                                "A pasta 'a_gravar' não contém arquivos de imagem.\n\nClique em OK para encerrar o programa.")
            subprocess.Popen("TASKKILL /F /IM EZCAD2.exe", shell=True)  # Fecha o processo do EZCAD2
            return False

        return True

    def iniciar_ezcad2():

        if cancelado:
            return

        # Capturar os valores inseridos nos campos de entrada
        posicao_x = entrada_posicao_x.get()
        posicao_y = entrada_posicao_y.get()
        tamanho_x = entrada_tamanho_x.get()
        tamanho_y = entrada_tamanho_y.get()
        definicao_x = entrada_definicao_x.get()
        definicao_y = entrada_definicao_y.get()

        # Verificar se todos os campos estão preenchidos
        if not (posicao_x and posicao_y and tamanho_x and tamanho_y and definicao_x and definicao_y):
            messagebox.showerror("Erro", "Todos os campos devem estar preenchidos!")
            return  # Sai da função se algum campo estiver vazio

        # Verificar se os valores inseridos são numéricos (incluindo negativos)
        if not (posicao_x.replace("-", "").isdigit() and posicao_y.replace("-", "").isdigit() and
                tamanho_x.replace("-", "").isdigit() and tamanho_y.replace("-", "").isdigit() and
                definicao_x.replace("-", "").isdigit() and definicao_y.replace("-", "").isdigit()):
            messagebox.showerror("Erro", "Todos os campos devem ser numéricos!")
            return  # Sai da função se algum valor não for numérico

        # Criar um elemento raiz para o arquivo XML
        root = Element("coordenadas")
        # Adicionar subelementos para as coordenadas
        SubElement(root, "posicao_x").text = posicao_x
        SubElement(root, "posicao_y").text = posicao_y
        SubElement(root, "tamanho_x").text = tamanho_x
        SubElement(root, "tamanho_y").text = tamanho_y
        SubElement(root, "definicao_x").text = definicao_x
        SubElement(root, "definicao_y").text = definicao_y

        # Criar o arquivo XML
        with open("coordenadas.xml", "wb") as f:
            f.write(tostring(root))

        # Abrir o aplicativo EZCAD2
        caminho_ezcad_exe = "EzCad2.exe"
        subprocess.Popen([caminho_ezcad_exe])
        time.sleep(2)
        pyautogui.press('space')
        janela.withdraw() #100%
        time.sleep(2)  # Lembrar de mudar para 15 segundos
        definicoes_ini()

        # Verificar se há arquivos na pasta a_gravar antes de mover
        if verificar_pastas():
            executar_comandos_clique()
            return

        # Fechar a janela tkinter se o botão Cancelar não tiver sido clicado
        if not cancelado:
            cancelar()

    def deletar_arquivo_da_tela():
        time.sleep(0.5)
        pyautogui.press('delete')

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
            if locations[0].any():
                y, x = locations[0][0], locations[1][0]
                # Clica acima 2 campos no position X
                tamanho_horizontal, tamanho_vertical = pyautogui.size()
                novo_x = min(x + 490, tamanho_horizontal + 330)
                novo_y = min(y + 330, tamanho_vertical - 50)
                pyautogui.click(x=novo_x, y=novo_y)
                pyautogui.press('delete')

    def mover_arquivos_gravados():
        if verificar_pastas():
            pasta_a_gravar = "a_gravar"
            pasta_gravados = "gravados"

            arquivos = os.listdir(pasta_a_gravar)

            # Verificar se a pasta contém apenas o arquivo "QR5.ezd"
            if len(arquivos) == 1 and arquivos[0] == "QR5.ezd":
                messagebox.showinfo("Atenção",
                                    "A pasta 'a_gravar' não tem mais arquivos de imagem.\n\nO programa será encerrado.")
                subprocess.Popen("TASKKILL /F /IM EZCAD2.exe", shell=True)  # Encerra o processo do EZCAD2
                sys.exit()  # Encerra o programa

            for arquivo in arquivos:
                if arquivo == "QR5.ezd":  # Se for "QR5.ezd", continue para o próximo arquivo
                    continue

                arquivo_origem = os.path.join(pasta_a_gravar, arquivo)
                arquivo_destino = os.path.join(pasta_gravados, arquivo)

                if os.path.exists(arquivo_destino):
                    mensagem = f"O arquivo '{arquivo}' já existe na pasta de destino e será sobrescrito."
                    messagebox.showinfo("Arquivo Duplicado", mensagem)
                    os.remove(arquivo_destino)

                draw()
                time.sleep(0.3)
                xey()
                time.sleep(0.3)
                aguardar_ok()
                encontrando_tarja()
                deletar_arquivo_da_tela()
                # Aqui movemos o arquivo para a pasta "gravados"
                os.rename(arquivo_origem, arquivo_destino)

            os.remove('screenshot_temp.png')  # ALTERAÇÃO PÓS 100%
            messagebox.showinfo("Concluído", "Todos os arquivos foram gravados.\n\nO programa será encerrado.")
            subprocess.Popen("TASKKILL /F /IM EZCAD2.exe", shell=True)
            cancelar()

    def encontrando_tarja():
        caminho_stop = 'stop.png'
        template = cv2.imread(caminho_stop, cv2.IMREAD_GRAYSCALE)

        while True:
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            locations = np.where(result >= threshold)

            if locations[0].any():
                break

        while True:
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= threshold)

            if not locations[0].any():
                break

            time.sleep(0.5)

    def n_lista_nome():
        pasta_a_gravar = "a_gravar"
        arquivos = os.listdir(pasta_a_gravar)

        return arquivos

    def draw():
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
            y, x = locations[0][0], locations[1][0]
            pyautogui.click(x=x, y=y)
            time.sleep(0.3)
            pyautogui.press('b')
            time.sleep(0.3)

            nomes_arquivos = n_lista_nome()
            for nome_arquivo in nomes_arquivos:
                pyautogui.write(nome_arquivo)
                pyautogui.press('enter')

    def xey():
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
        threshold = 0.7
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
                # time.sleep(0.3)
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

    def aguardar_ok():
        pyautogui.alert("Pressione OK para continuar...")
        pyautogui.hotkey("f2")

    def executar_comandos_clique():
        if not cancelado:
            mover_arquivos_gravados()


    # Criar a janela principal
    janela = Tk()
    janela.title("EZCAD2")

    # Definir as dimensões da janela
    largura_janela = 220
    altura_janela = 260

    # Obter as dimensões da tela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Calcular as coordenadas para a janela aparecer no centro da tela
    x_pos = (largura_tela - largura_janela) // 2
    y_pos = (altura_tela - altura_janela) // 2

    # Definir a posição da janela
    posicao_janela = f"{largura_janela}x{altura_janela}+{x_pos}+{y_pos}"
    janela.geometry(posicao_janela)

    # Define a cor de fundo da janela
    janela.configure(bg="#dde")

    # Impede que a janela seja redimensionada
    janela.resizable(False, False)

    # Criar um Canvas para desenhar a borda
    canvas = Canvas(janela, highlightthickness=0, bg="#dde")
    canvas.pack(fill=BOTH, expand=True)

    # Criar os rótulos e campos de entrada
    rotulo_posicao_x = Label(janela, bg="#dde", text="Posição X:")
    rotulo_posicao_x.place(x=20, y=20)
    entrada_posicao_x = Entry(janela, width=10)
    entrada_posicao_x.place(x=100, y=20)

    rotulo_posicao_y = Label(janela, bg="#dde", text="Posição Y:")
    rotulo_posicao_y.place(x=20, y=50)
    entrada_posicao_y = Entry(janela, width=10)
    entrada_posicao_y.place(x=100, y=50)

    rotulo_tamanho_x = Label(janela, bg="#dde", text="Tamanho X:")
    rotulo_tamanho_x.place(x=20, y=80)
    entrada_tamanho_x = Entry(janela, width=10)
    entrada_tamanho_x.place(x=100, y=80)

    rotulo_tamanho_y = Label(janela, bg="#dde", text="Tamanho Y:")
    rotulo_tamanho_y.place(x=20, y=110)
    entrada_tamanho_y = Entry(janela, width=10)
    entrada_tamanho_y.place(x=100, y=110)

    rotulo_definicao_x = Label(janela, bg="#dde", text="Definição X:")
    rotulo_definicao_x.place(x=20, y=140)
    entrada_definicao_x = Entry(janela, width=10)
    entrada_definicao_x.place(x=100, y=140)

    rotulo_definicao_y = Label(janela, bg="#dde", text="Definição Y:")
    rotulo_definicao_y.place(x=20, y=170)
    entrada_definicao_y = Entry(janela, width=10)
    entrada_definicao_y.place(x=100, y=170)

    # Botões de iniciar e cancelar
    botao_iniciar = Button(janela, text="Iniciar", command=iniciar_ezcad2, bg="#4CAF50", fg="white")
    botao_iniciar.place(x=30, y=210, width=70)

    botao_cancelar = Button(janela, text="Cancelar", command=cancelar, bg="#FF5733", fg="white")
    botao_cancelar.place(x=120, y=210, width=70)

    janela.mainloop()


main()  # Chamada para iniciar o programa