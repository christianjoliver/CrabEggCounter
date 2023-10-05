import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import eggcounter as ec
import os

arr_images = []
arr_name_images = []

flag_ed = False
scale = 0.4  # Escala inicial

def resize(event):
    # Função para ajustar o tamanho do frame quando a janela é redimensionada
    frame.config(width=event.width, height=event.height)
    resize_image()

def resize_image():
    if arr_images:
        # Redimensiona a imagem com base na escala atual
        
        image = arr_images[-1]
        resized_width = int(image.shape[1] * scale)
        resized_height = int(image.shape[0] * scale)
        resized_image = cv2.resize(image, (resized_width, resized_height))
        
        # Converte a imagem para o formato RGB usando o Pillow (PIL)
        image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        image_pillow = Image.fromarray(image_rgb)
        
        # Converte a imagem para um formato que o Tkinter possa exibir
        image_tk = ImageTk.PhotoImage(image_pillow)
        
        # Atualiza o rótulo com a nova imagem
        image_label.config(image=image_tk)
        image_label.image = image_tk  # Mantém uma referência para evitar que a imagem seja destruída pelo coletor de lixo


def load_image():
    # Abre uma caixa de diálogo do explorador de arquivos
    file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.gif")])

    # Verifica se o usuário selecionou um arquivo
    if file_path:
        # Lê a imagem usando cv2.imread
        image = cv2.imread(file_path)
        image, qnt = ec.CrabbEggDetection(image)
        arr_images.append(image)
        arr_name_images.append(os.path.basename(file_path))
        
        # Redimensiona a imagem com base na escala atual
        resize_image()
        tk.messagebox.showinfo("Informação", "Imagem carregada!")


def block_loading():

    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
    # Abre uma caixa de diálogo no explorador de arquivos solicitando uma pasta contendo o bloco de imagens
    directory_path = filedialog.askdirectory(title="Escolha o diretório")

    # Itera sobre os itens da pasta
    if directory_path:
        files_in_directory = os.listdir(directory_path)
        arr_image_paths = [os.path.join(directory_path, file) for file in files_in_directory if file.lower().endswith(image_extensions)]

        for file_path in arr_image_paths:
             image = cv2.imread(file_path)
             image, qnt = ec.CrabbEggDetection(image)
             arr_images.append(image)
             arr_name_images.append(os.path.basename(file_path))
        tk.messagebox.showinfo("Informação", "Imagens contadas com sucesso")

def open_destination_folder():
    if not arr_images or not flag_ed:
        # Mostra uma mensagem de alerta se nenhum dado foi exportado ainda
        tk.messagebox.showinfo("Alerta", "Nenhum dado foi exportado ainda. Por favor, exporte os dados primeiro.")
        return

    # Abre a pasta de destino no explorador de arquivos do sistema
    path = os.path.realpath(export_dir)
    os.startfile(path)


def export_data():

    global export_dir

    if not arr_images:
        tk.messagebox.showinfo("Alerta", "Nenhuma imagem carregada.")
        return

    # Abre uma caixa de diálogo para escolher o diretório de exportação
    export_dir = filedialog.askdirectory(title="Escolher diretório de exportação")
    
    # Verifica se o usuário selecionou um diretório
    if export_dir:
        # Itera sobre todas as imagens e as exporta para o diretório escolhido
        for i, image in enumerate(arr_images):
            arq_name = f"{arr_name_images[i]}"  # Nome do arquivo
            arq_path = os.path.join(export_dir, arq_name)
            cv2.imwrite(arq_path, image)
        tk.messagebox.showinfo("Informação", "Dados exportados com sucesso!")
        global flag_ed
        flag_ed = True


def scroll(event):
    global scale
    if arr_images:
        # Atualiza a escala com base na direção do scroll do mouse
        if event.delta > 0:
            scale *= 1.1  # Aumenta a escala em 10%
        else:
            scale /= 1.1  # Diminui a escala em 10%
        
        # Limita a escala mínima e máxima
        scale = max(0.4, min(2.0, scale))  # Limite a escala entre 10% e 200%
        
        # Redimensiona a imagem com base na nova escala
        resize_image()

# Cria a janela principal
root = tk.Tk()
root.title("EggCounter")
root.geometry("1024x650")  # Tamanho inicial da janela

# Cria o frame
frame = tk.Frame(root, bg="#9C9C9C")
frame.pack(fill=tk.BOTH, expand=True)

# Associa a função de redimensionamento à janela
root.bind("<Configure>", resize)

# Cria a barra de tarefas superior com os botões
toolbar = tk.Frame(frame, bg="#FFFFFF")
toolbar.pack(side=tk.TOP, fill=tk.X)

# Botão "Carregar Imagem"
load_image_button = tk.Button(toolbar, text="Carregar Imagem", command=load_image, bg="#FFFFFF", highlightthickness=0)
load_image_button.pack(side=tk.LEFT, padx=1)

# Botão "Carregamento em Bloco"
block_loading_button = tk.Button(toolbar, text="Carregamento em Bloco", command=block_loading, bg="#FFFFFF", highlightthickness=0)
block_loading_button.pack(side=tk.LEFT, padx=1)

# Botão "Exportar Dados"
export_data_button = tk.Button(toolbar, text="Exportar Dados", command=export_data, bg="#FFFFFF", highlightthickness=0)
export_data_button.pack(side=tk.LEFT, padx=1)

# Botão "Abrir Pasta de Desino"
open_destination_folder_button = tk.Button(toolbar, text="Abrir Pasta de Desino", command=open_destination_folder, bg="#FFFFFF", highlightthickness=0)
open_destination_folder_button.pack(side=tk.LEFT, padx=1)

# Cria o rótulo para exibir a imagem e adiciona o evento de rolagem
image_label = tk.Label(frame)
image_label.pack(side=tk.RIGHT)  # Alinha o rótulo à direita do frame
image_label.bind("<MouseWheel>", scroll)  # Adiciona evento de rolagem

# Cria o rótulo para exibir a imagem e adiciona o evento de rolagem
info_label = tk.Label(frame)
info_label.pack(side=tk.LEFT)  # Alinha o rótulo à direita do frame


root.resizable(False, False)

root.mainloop()
