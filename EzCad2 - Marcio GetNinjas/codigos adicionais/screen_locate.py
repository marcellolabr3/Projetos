import time

import cv2
import numpy as np

# Carregar a imagem principal e o template
screenshot = cv2.imread('screenshot_temp.png')
template = cv2.imread('template.png')

# Definir a região de interesse (ROI)
# Aqui, definimos manualmente as coordenadas do canto superior esquerdo (x, y)
# e a largura e altura da ROI
x, y, w, h = 200, 200, 100, 100  # Exemplo de coordenadas e tamanho da ROI
roi = screenshot[y:y+h, x:x+w]

# Realizar a correspondência de padrões apenas na região de interesse (ROI)
resultado = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)

# Encontrar os locais onde a correspondência atende ao threshold
threshold = 0.5
locations = np.where(resultado >= threshold)

# Iterar sobre os locais encontrados e fazer algo com eles
for pt in zip(*locations[::-1]):
    # pt é a coordenada do canto superior esquerdo onde o padrão foi encontrado
    cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

# Exibir a imagem com as áreas de correspondência destacadas

cv2.imshow('Resultado', screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()
