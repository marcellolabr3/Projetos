import shutil
import sys
import tkinter as tk
from tkinter import messagebox
import pyautogui
import os
import subprocess
import time
import cv2
import numpy as np
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
import threading

class EZCAD2:
    arquivos_a_gravar = []
    diretorio_atual = os.path.dirname(os.path.abspath(sys.argv[0]))
    arquivo_gravar = os.path.join(diretorio_atual, 'a_gravar')
    pasta_a_gravar = "a_gravar"
    pasta_gravados = "gravados"

    def __init__(self):
        self.cancelado = False
        self.posicao_x = None
        self.posicao_y = None
        self.tamanho_x = None
        self.tamanho_y = None
        self.definicao_x = None
        self.definicao_y = None

        # Chamar o método para ler os dados do XML e armazená-los nas variáveis
        self.ler_dados_xml()

    def ler_dados_xml(self):
        try:
            # Verificar se o arquivo XML existe
            if os.path.exists("coordenadas.xml"):
                valores_xml = ET.parse('coordenadas.xml').getroot()
                self.posicao_x = int(valores_xml.find('posicao_x').text)
                self.posicao_y = int(valores_xml.find('posicao_y').text)
                self.tamanho_x = int(valores_xml.find('tamanho_x').text)
                self.tamanho_y = int(valores_xml.find('tamanho_y').text)
                self.definicao_x = int(valores_xml.find('definicao_x').text)
                self.definicao_y = int(valores_xml.find('definicao_y').text)
        except Exception as e:
            # Lidar com exceções ao ler o arquivo XML
            messagebox.showerror("Erro", f"Erro ao ler arquivo XML: {e}")

    def iniciar_ezcad2(self):

        if self.cancelado:
            return

        # Capturar os valores inseridos nos campos de entrada
        self.posicao_x = self.entrada_posicao_x.get()
        self.posicao_y = self.entrada_posicao_y.get()
        self.tamanho_x = self.entrada_tamanho_x.get()
        self.tamanho_y = self.entrada_tamanho_y.get()
        self.definicao_x = self.entrada_definicao_x.get()
        self.definicao_y = self.entrada_definicao_y.get()

        # Criar um elemento raiz para o arquivo XML
        root = Element("coordenadas")
        # Adicionar subelementos para as coordenadas
        SubElement(root, "posicao_x").text = self.posicao_x
        SubElement(root, "posicao_y").text = self.posicao_y
        SubElement(root, "tamanho_x").text = self.tamanho_x
        SubElement(root, "tamanho_y").text = self.tamanho_y
        SubElement(root, "definicao_x").text = self.definicao_x
        SubElement(root, "definicao_y").text = self.definicao_y

        # Verificar se todos os campos estão preenchidos
        if not (
                self.posicao_x and self.posicao_y and self.tamanho_x and self.tamanho_y and self.definicao_x and self.definicao_y):
            messagebox.showerror("Erro", "Todos os campos devem estar preenchidos!")
            return

        # Verificar se os valores inseridos são numéricos (incluindo negativos)
        if not (self.posicao_x.replace("-", "").isdigit() and self.posicao_y.replace("-", "").isdigit() and
                self.tamanho_x.replace("-", "").isdigit() and self.tamanho_y.replace("-", "").isdigit() and
                self.definicao_x.replace("-", "").isdigit() and self.definicao_y.replace("-", "").isdigit()):
            messagebox.showerror("Erro", "Todos os campos devem ser numéricos!")
            return

        # Criar o arquivo XML
        with open("coordenadas.xml", "wb") as f:
            f.write(tostring(root))

        # Abrir o aplicativo EZCAD2
        caminho_ezcad_exe = "EzCad2.exe"
        subprocess.Popen([caminho_ezcad_exe])
        time.sleep(2)
        pyautogui.press('space')
        self.janela.withdraw()  # 100%
        time.sleep(2)  # Lembrar de mudar para 15 segundos
        self.definicoes_ini()

        if self.verificar_pastas():
            self.extrai_nomes()
            self.executar_clique()

        if not self.cancelado:
            self.cancelar()

    def __delattr__(self, __name):
        super().__delattr__(__name)

    def definicoes_ini(self):
        time.sleep(0.7)
        pyautogui.hotkey('ctrl', 'o')
        time.sleep(0.5)
        qr5 = os.path.join(self.diretorio_atual, 'QR5.ezd')
        pyautogui.write(qr5)
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

    def verificar_pastas(self):

        if not os.path.exists(self.pasta_a_gravar):
            os.makedirs(self.pasta_a_gravar)

        if not os.path.exists(self.pasta_gravados):
            os.makedirs(self.pasta_gravados)

        # Se a lista estiver vazia, significa que ainda não foi preenchida
        self.arquivos_a_gravar = [arquivo.name for arquivo in os.scandir(self.pasta_a_gravar)]

        return True

    def extrai_nomes(self):
        arquivo_texto = "arquivo_texto.txt"

        # Salva os nomes dos arquivos em um arquivo de texto
        with open(arquivo_texto, 'w') as file:
            for nome_arquivo in self.arquivos_a_gravar:
                file.write(nome_arquivo + '\n')

        with open("arquivo_texto.txt", 'r') as file:
            arquivos_texto = file.read().splitlines()

        if not arquivos_texto:
            messagebox.showinfo("Atenção",
                                "A pasta 'a_gravar' não contém arquivos de imagem.\n\nClique em OK para encerrar o programa.")
            self.janela.quit()
            subprocess.Popen("TASKKILL /F /IM Auto EzCad2.exe", shell=True) #Trocar pelo nome da aplicação
            return False

        return True

    def executar_clique(self):
        if not self.cancelado:
            self.mover_arquivos_gravados()

    def cancelar(self):
        self.cancelado = True
        self.janela.quit()
        subprocess.Popen("TASKKILL /F /IM Auto EzCad2.exe", shell=True) #Trocar pelo nome da aplicação

    def mover_arquivos_gravados(self):

        if self.extrai_nomes():

            # Verifica se a condição é verdadeira com base no conteúdo do arquivo de texto
            with open("arquivo_texto.txt", 'r') as file:
                arquivos_texto = file.read().splitlines()

            if not arquivos_texto:
                messagebox.showinfo("Atenção",
                                    "A pasta 'a_gravar' não tem mais arquivos de imagem.\n\nO programa será encerrado.")
                self.janela.quit()
                subprocess.Popen("TASKKILL /F /IM Auto EzCad2.exe", shell=True) #Trocar pelo nome da aplicação
                return

            self.compilado()
            messagebox.showinfo("Concluído", "Todos os arquivos foram gravados.\n\nO programa será encerrado.")
            self.janela.quit()
            subprocess.Popen("TASKKILL /F /IM Auto EzCad2.exe", shell=True) #Trocar pelo nome da aplicação
            self.cancelar()

    def compilado(self):

        self.draw()
        self.fast_execute()

    def tarja_ou_ok(self):
        # Loop infinito para monitorar a tela
        nomes_arquivos = ['marking1360.png', 'marking1920.png']
        while True:
            screenshot = pyautogui.screenshot()
            screenshot_cv = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
            cv2.imwrite('screenshot_temp.png', screenshot_cv)
            screenshot = cv2.imread('screenshot_temp.png')

            for caminho_arquivo in nomes_arquivos:
                template = cv2.imread(caminho_arquivo)
                print(f"Lendo o arquivo: {caminho_arquivo}")

                if template is not None:
                    resultado = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.7
                    locations = np.where(resultado >= threshold)
                    print(f"Arquivo {caminho_arquivo} carregado com sucesso.")

                    if locations[0].any():
                        y, x = locations[0][0], locations[1][0]
                        tamanho_horizontal, tamanho_vertical = pyautogui.size()
                        novo_x = min(x + 255, tamanho_horizontal - 200)
                        novo_y = min(y + 150, tamanho_vertical - 0)
                        pyautogui.moveTo(x=novo_x, y=novo_y)
                        print(f"Correspondência encontrada para o arquivo: {caminho_arquivo}")
                        pyautogui.click()
                        return False
                    else:
                        print('nao achei')
            time.sleep(0.5)  # Pausa por 0.5 segundos antes de verificar novamente

    def aguardar_ok(self):
        pyautogui.alert(text='Pressione OK para continuar...', title='Aguardando continuar')
        pyautogui.hotkey("f2")

    def fast_execute(self):

        with open("arquivo_texto.txt", 'r') as file:
            arquivos_texto = file.read().splitlines()

        for arquivo_texto in arquivos_texto:
            pyautogui.write(self.arquivo_gravar + "\\" + arquivo_texto)
            pyautogui.press('enter')
            time.sleep(0.5)
            self.xey()
            time.sleep(0.5)
            #thread para monitorar a tela
            monitor_thread = threading.Thread(target=self.tarja_ou_ok)
            monitor_thread.start()
            self.aguardar_ok()
            self.encontrando_tarja()
            self.deletar_arquivo_da_tela()
            arquivo_origem = os.path.join(self.pasta_a_gravar, arquivo_texto)
            arquivo_destino = os.path.join(self.pasta_gravados, arquivo_texto)
            shutil.move(arquivo_origem, arquivo_destino)
            time.sleep(0.5)
            self.draw()

    def draw(self):
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

    def xey(self):
        try:
            screenshot = pyautogui.screenshot()
            screenshot_cv = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
            cv2.imwrite('screenshot_temp.png', screenshot_cv)
            screenshot = cv2.imread('screenshot_temp.png')
            nomes_arquivos = ['xey1360.png', 'xey21360.png', 'xey1920.png', 'xey21920.png']
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
                        novo_x = min(x + 25, tamanho_horizontal - 30)
                        novo_y = min(y - 60, tamanho_vertical - 50)
                        pyautogui.doubleClick(x=novo_x, y=novo_y)
                        pyautogui.write(str(self.posicao_x))
                        pyautogui.press('tab')
                        pyautogui.write(str(self.posicao_y))
                        pyautogui.press('tab')
                        pyautogui.write(str(self.tamanho_x))
                        pyautogui.press('tab')
                        pyautogui.write(str(self.tamanho_y))
                        tamanho_horizontal, tamanho_vertical = pyautogui.size()
                        novo_x = min(x + 120, tamanho_horizontal - 50)
                        novo_y = min(y + 98, tamanho_vertical - 50)
                        pyautogui.doubleClick(x=novo_x, y=novo_y)
                        pyautogui.write(str(self.definicao_x))
                        novo_y += 20
                        pyautogui.doubleClick(x=novo_x, y=novo_y)
                        pyautogui.write(str(self.definicao_y))
                        time.sleep(0.3)
                        pyautogui.hotkey('alt', 'a')
                        return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar: {e}")
            return None
        return False

    def encontrando_tarja(self):
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

    def deletar_arquivo_da_tela(self):
        time.sleep(0.5)
        pyautogui.press('delete')

    def criar_janela(self):
        self.janela = tk.Tk()
        self.janela.title("EZCAD2")
        largura_janela = 220
        altura_janela = 260
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()
        x_pos = (largura_tela - largura_janela) // 2
        y_pos = (altura_tela - altura_janela) // 2
        posicao_janela = f"{largura_janela}x{altura_janela}+{x_pos}+{y_pos}"
        self.janela.geometry(posicao_janela)
        self.janela.configure(bg="#dde")
        self.janela.resizable(False, False)
        canvas = tk.Canvas(self.janela, highlightthickness=0, bg="#dde")
        canvas.pack(fill=tk.BOTH, expand=True)
        # Rótulos para os campos de entrada
        tk.Label(self.janela, bg="#dde", text="Posição X:").place(x=10, y=20)
        tk.Label(self.janela, bg="#dde", text="Posição Y:").place(x=10, y=50)
        tk.Label(self.janela, bg="#dde", text="Tamanho X:").place(x=10, y=80)
        tk.Label(self.janela, bg="#dde", text="Tamanho Y:").place(x=10, y=110)
        tk.Label(self.janela, bg="#dde", text="Definição X:").place(x=10, y=140)
        tk.Label(self.janela, bg="#dde", text="Definição Y:").place(x=10, y=170)

        self.entrada_posicao_x = tk.Entry(self.janela, width=10)
        self.entrada_posicao_x.place(x=100, y=20)
        self.entrada_posicao_y = tk.Entry(self.janela, width=10)
        self.entrada_posicao_y.place(x=100, y=50)
        self.entrada_tamanho_x = tk.Entry(self.janela, width=10)
        self.entrada_tamanho_x.place(x=100, y=80)
        self.entrada_tamanho_y = tk.Entry(self.janela, width=10)
        self.entrada_tamanho_y.place(x=100, y=110)
        self.entrada_definicao_x = tk.Entry(self.janela, width=10)
        self.entrada_definicao_x.place(x=100, y=140)
        self.entrada_definicao_y = tk.Entry(self.janela, width=10)
        self.entrada_definicao_y.place(x=100, y=170)
        botao_iniciar = tk.Button(self.janela, text="Iniciar", command=self.iniciar_ezcad2, bg="#4CAF50", fg="white")
        botao_iniciar.place(x=30, y=210, width=70)
        botao_cancelar = tk.Button(self.janela, text="Cancelar", command=self.cancelar, bg="#FF5733", fg="white")
        botao_cancelar.place(x=120, y=210, width=70)

        self.janela.mainloop()


if __name__ == "__main__":
    ezcad2 = EZCAD2()
    ezcad2.criar_janela()

