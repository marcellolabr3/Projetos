import os
from tkinter import messagebox


def verificar_pastas():
    try:
        pasta_a_gravar = "a_gravar"
        pasta_gravados = "gravados"

        if not os.path.exists(pasta_a_gravar):
            os.makedirs(pasta_a_gravar)

        if not os.path.exists(pasta_gravados):
            os.makedirs(pasta_gravados)


        # Lista os nomes dos arquivos na pasta especificada
        lista_arquivos = os.listdir(pasta_a_gravar)
        # Se houver apenas o arquivo "QR5.ezd", informa que não há arquivos de imagem e retorna False
        if len(lista_arquivos) == 1 and lista_arquivos[0] == "QR5.ezd":
            print("Não há arquivos de imagem na pasta 'a_gravar'.")
            return False
        # Se houver outros arquivos além de "QR5.ezd", salva os nomes dos arquivos (exceto "QR5.ezd") em um arquivo de texto
        else:
            with open('lista_arquivos.txt', 'w') as file:
                for arquivo in lista_arquivos:
                    if arquivo != "QR5.ezd":
                        file.write(arquivo + '\n')
            return True
    except FileNotFoundError:
        messagebox.showinfo("Atenção",
                            f"A pasta 'a_gravar' não foi encontrada.\n\nClique em OK para encerrar o programa.")
        # subprocess.Popen("TASKKILL /F /IM EZCAD2.exe", shell=True)
        return False

# Chamada da função para verificar as pastas
if not verificar_pastas():
    messagebox.showinfo("Atenção",
                        "A pasta 'a_gravar' não contém arquivos de imagem.\n\nClique em OK para encerrar o programa.")
    # subprocess.Popen("TASKKILL /F /IM EZCAD2.exe", shell=True)