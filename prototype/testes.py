# Código Referente aos testes da técnica de ROI                     (V3)                             ##############################                    MAIS PROMISSOR                       #########################
import cv2
import numpy as np


escala_atual = 1.0

def redimensionar_imagem(nova_escala):
    global escala_atual
    escala_atual = nova_escala
    nova_largura = int(img.shape[1] * escala_atual)
    nova_altura = int(img.shape[0] * escala_atual)
    img_redimensionada = cv2.resize(img, (nova_largura, nova_altura))
    cv2.imshow("Imagem com Círculos", img_redimensionada)


def mouse_callback(event, x, y, flags, param):
    global escala_atual
    if event == cv2.EVENT_MOUSEWHEEL:
        delta = flags >> 16  # Obtém o valor do scroll do mouse
        nova_escala = escala_atual + delta * 0.001  # Ajuste a velocidade de zoom conforme necessário
        nova_escala = max(0.1, nova_escala)  # Defina um limite mínimo
        nova_escala = min(1.0, nova_escala)  # Defina um limite máximo
        if nova_escala != escala_atual:
            redimensionar_imagem(nova_escala)


# Ler a imagem.
img = cv2.imread('C:/Users/alunos/Documents/Christian/projeto/img_test/img3.jpg', cv2.IMREAD_UNCHANGED)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Defina os intervalos de cores que você deseja segmentar (tons de laranja)
lower_color = np.array([0, 80, 80])  # Valor mínimo do matiz, saturação e luminosidade
upper_color = np.array([25, 255, 255])  # Valor máximo do matiz, saturação e luminosidade

mask = cv2.inRange(hsv, lower_color, upper_color)
result = cv2.bitwise_and(img, img, mask=mask)

cinza = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

cinza_desfocado = cv2.medianBlur(cinza, 7)

# Aplicar transformada de Hough na imagem desfocada.

circulos_detectados = cv2.HoughCircles(cinza_desfocado, cv2.HOUGH_GRADIENT, 1, 35, param1 = 1, param2 = 30, minRadius = 10, maxRadius = 39)


# Desenhar os círculos detectados.
if circulos_detectados is not None:
    qnt = 0;
    # Converter os parâmetros do círculo (a, b e r) para inteiros.
    circulos_detectados = np.uint16(np.around(circulos_detectados))

    for idx, pt in enumerate(circulos_detectados[0, :]):
        qnt = qnt+1
        a, b, r = pt[0], pt[1], pt[2]

        # Desenhar a circunferência do círculo.
        cv2.circle(img, (a, b), 20, (0, 0, 255), 1)

        fontScale = 0.5  # Ajuste o valor para alterar o tamanho da fonte
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = str(idx+1)
        textSize = cv2.getTextSize(text, font, fontScale, 1)[0]
        textX = int(a - textSize[0] / 2)
        textY = int(b + textSize[1] / 2)
        cv2.putText(img, text, (textX, textY), font, fontScale, (0, 255, 0), 1)

    print(qnt)
    # Mostrar a imagem com os círculos desenhados.
    cv2.namedWindow("Imagem com Círculos")
    cv2.imshow("Imagem com Círculos", img)
    cv2.setMouseCallback("Imagem com Círculos", mouse_callback)

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()

