# Código Referente aos testes da técnica de ROI                     (V3)                             ##############################                    MAIS PROMISSOR                       #########################
import cv2
import numpy as np

def CrabbEggDetection(img):
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

    return img, qnt