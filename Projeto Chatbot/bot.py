import os
import time
import re
import requests
import urllib3
import json
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class wppbot:

    dir_path = os.getcwd()

    def __init__(self, nome_bot):
        print(self.dir_path)
        self.bot = ChatBot(nome_bot)
        self.conversas_treinadas = []
        self.bot.set_trainer(ListTrainer)

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.chrome = os.path.join(self.dir_path, 'chromedriver.exe')

        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir=" + self.dir_path + r"\\profile\\wpp")

        # Use 'options' em vez de 'chrome_options'
        self.driver = webdriver.Chrome(options=self.options)

    def inicia(self, nome_contato):
        self.driver.get('https://web.whatsapp.com/')

        # Define um tempo de espera máximo
        max_wait_time = 60  # 60 segundos

        # Verifica se a página está carregada pela primeira vez
        first_load = True

        # Verifica se o QR code está presente somente na primeira carga da página
        while first_load:
            try:
                time.sleep(3)
                # Verifica se o QR code está presente
                qr_code_elements = self.driver.find_elements(By.XPATH,
                                                             '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas')
                if len(qr_code_elements) < 1:
                    print("QR code não encontrado. Continuando sem autenticação.")
                    break  # Se o QR code não estiver presente, sai do loop

                # Se o QR code estiver presente, espera até que o painel lateral seja carregado
                WebDriverWait(self.driver, max_wait_time).until(EC.presence_of_element_located((By.ID, 'side')))
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
                WebDriverWait(self.driver, max_wait_time).until(EC.presence_of_element_located((By.ID, 'side')))
            except TimeoutException:
                print("Tempo máximo de espera excedido. Continuando sem autenticação.")
            except Exception as e:
                print("Erro ao carregar o WhatsApp Web:", e)

        try:
            # Espera até que o elemento esteja presente no DOM da página
            elemento_presente = WebDriverWait(self.driver, max_wait_time).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
            )

            # Localiza a caixa de pesquisa e envia o nome do contato
            self.caixa_de_pesquisa = elemento_presente
            self.caixa_de_pesquisa.send_keys(nome_contato, Keys.ENTER)
            time.sleep(2)


            return self.driver
        except Exception as e:
            print("deu ruim", e)
        except TimeoutException:
            print("Tempo máximo de espera excedido ao carregar o painel lateral.")

    def saudacao(self, frase_inicial):

        self.caixa_de_mensagem = self.driver.find_element(By.XPATH, '//div[@class="x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf"]')

        if type(frase_inicial) == list:
            for frase in frase_inicial:
                self.caixa_de_mensagem.send_keys(frase, Keys.ENTER)
                time.sleep(1)
        else:
            return False

    def escuta(self):
        try:

            # Encontrar todas as mensagens do grupo
            mensagens = self.driver.find_elements(By.CLASS_NAME, '_akbu')

            # Verificar se existem mensagens
            if mensagens:
                # Pegar a última mensagem (que é a mais recente)
                ultima_mensagem = mensagens[-1]

                # Encontrar o elemento de texto dentro da última mensagem
                elemento_texto = ultima_mensagem.find_element(By.XPATH, './/span[contains(@class, "_ao3e") and contains(@class, "selectable-text") and contains(@class, "copyable-text")]')


                # Obter o texto do elemento da mensagem
                texto = elemento_texto.text

                print("Texto da última mensagem:", texto)  # Debugging

                return texto
            else:
                print("Nenhuma mensagem encontrada.")
                return None
        except NoSuchElementException:
                print("Elemento de mensagem não encontrado.")
                return None


    def aprender(self, ultimo_texto, frase_inicial, frase_final, frase_erro):
        self.caixa_de_mensagem = self.driver.find_element(By.XPATH, '//div[@class="x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf"]')
        self.caixa_de_mensagem.send_keys(frase_inicial, Keys.ENTER)
        time.sleep(1)
        self.x = True
        while self.x:
            texto = self.escuta()

            if texto != ultimo_texto and re.match(r'^::', texto):
                if '?' in texto:
                    ultimo_texto = texto
                    texto = texto.replace('::', '').lower().replace('?', '?*').split('*')
                    novo = [elemento.strip() for elemento in texto]

                    self.bot.train(novo)
                    self.caixa_de_mensagem.send_keys(frase_final, Keys.ENTER)
                    time.sleep(1)
                    self.x = False
                    return ultimo_texto
                else:
                    self.caixa_de_mensagem.send_keys(frase_erro, Keys.ENTER)
                    time.sleep(1)
                    self.x = False
                    return ultimo_texto
            else:
                ultimo_texto = texto

    def noticias(self):

        req = requests.get('https://newsapi.org/v2/top-headlines?sources=globo&pageSize=5&apiKey=f6fdb7cb0f2a497d92dbe719a29b197f')
        noticias = json.loads(req.text)

        for news in noticias['articles']:
            titulo = news['title']
            link = news['url']
            new = 'bot: ' + titulo + ' ' + link + '\n'

            self.caixa_de_mensagem.send_keys(new)
            time.sleep(1)

    def responde(self, texto):
        response = self.bot.get_response(texto)
        # if float(response.confidence) > 0.5:
        response = str(response)
        response = 'bot: ' + response
        self.caixa_de_mensagem = self.driver.find_element(By.XPATH, '//div[@class="x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf"]')
        self.caixa_de_mensagem.send_keys(response, Keys.ENTER)
        time.sleep(1)

    def treina(self, nome_pasta):
        # Verifica se a pasta de treino existe
        if not os.path.exists(nome_pasta):
            print("A pasta de treino não existe.")
            return

        # Carrega os nomes dos arquivos já treinados, se existirem
        if os.path.exists('conversas_treinadas.txt'):
            with open('conversas_treinadas.txt', 'r') as arquivo_treinado:
                conversas_treinadas = arquivo_treinado.read().splitlines()
        else:
            conversas_treinadas = []

        # Lista os arquivos na pasta de treino
        arquivos_na_pasta = os.listdir(nome_pasta)
        print("Arquivos na pasta de treino:", arquivos_na_pasta)

        novos_arquivos = [arquivo for arquivo in arquivos_na_pasta if arquivo not in conversas_treinadas]
        print("Novos arquivos a serem treinados:", novos_arquivos)

        if novos_arquivos:
            for arquivo in novos_arquivos:
                with open(os.path.join(nome_pasta, arquivo), 'r') as arquivo_aberto:
                    conversas = arquivo_aberto.readlines()
                    self.bot.train(conversas)
                    print("Arquivo", arquivo, "treinado com sucesso.")

            # Adiciona os novos arquivos treinados à lista de arquivos treinados
            conversas_treinadas.extend(novos_arquivos)

            # Salva os nomes dos arquivos treinados em um arquivo de texto
            with open('conversas_treinadas.txt', 'w') as arquivo_treinado:
                arquivo_treinado.write('\n'.join(conversas_treinadas))
        else:
            print("Nenhum arquivo novo encontrado para treinar.")

