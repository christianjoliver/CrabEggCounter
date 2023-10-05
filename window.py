import tkinter as tk
from tkinter import filedialog, messagebox, Label, Menu
from PIL import Image, ImageTk
import cv2
import eggcounter as ec
import os
import locale

# Configurar a codificação para UTF-8
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Configurar a variável de ambiente TK_SILENCE_DEPRECATION
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class Functions():
    arr_images = []
    arr_name_images = []
    arr_qnt = []
    export_data_flag = False
    load_flag = False
    qnt = 0;

    def resize_image(self, event=None):
        if self.arr_images:
            
            # Redimensiona a imagem com base na escala atual
            image = self.arr_images[-1]

            # Obtém as dimensões atuais do Label
            label_width = self.image_label.winfo_width()
            label_height = self.image_label.winfo_height()

            # Calcula as novas dimensões da imagem
            resized_width = label_width
            resized_height = label_height

            # Redimensiona a imagem
            resized_image = cv2.resize(image, (resized_width, resized_height))

            # Converte a imagem para o formato RGB usando o Pillow (PIL)
            image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
            image_pillow = Image.fromarray(image_rgb)

            # Converte a imagem para um formato que o Tkinter possa exibir
            image_tk = ImageTk.PhotoImage(image_pillow)

            # Atualiza o Label com a nova imagem
            self.image_label.config(image=image_tk)
            self.image_label.image = image_tk  # Mantém uma referência para evitar que a imagem seja destruída pelo coletor de lixo

    def update_info(self):
        self.info_num_label.config(text=f"Número de Ovos: {self.qnt}")
        self.info_name_label.config(text=f"Nome da Imagem: {self.arr_name_images[-1]}")

    def load_image(self):
        # Abre uma caixa de diálogo do explorador de arquivos
        file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.gif")])

        # Verifica se o usuário selecionou um arquivo
        if file_path:
            # Lê a imagem usando cv2.imread
            image = cv2.imread(file_path)

            # Aplica o método de Hough para contar os ovos e retorna a imagem contada
            image, self.qnt = ec.CrabbEggDetection(image)

            #Adiciona a imagem no array de imagens
            self.arr_images.append(image)
            self.arr_qnt.append(self.qnt)
            self.arr_name_images.append(os.path.basename(file_path))
            self.load_flag = True
            self.resize_image()
            
    def block_loading(self):

        self.arr_images.clear()
        self.arr_name_images.clear()
        self.arr_qnt.clear()

        image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
        # Abre uma caixa de diálogo no explorador de arquivos solicitando uma pasta contendo o bloco de imagens
        directory_path = filedialog.askdirectory(title="Escolha o diretório")

        # Itera sobre os itens da pasta
        if directory_path:
            files_in_directory = os.listdir(directory_path)
            arr_image_paths = [os.path.join(directory_path, file) for file in files_in_directory if file.lower().endswith(image_extensions)]

            for file_path in arr_image_paths:
                image = cv2.imread(file_path)
                image, self.qnt = ec.CrabbEggDetection(image)
                self.arr_images.append(image)
                self.arr_name_images.append(os.path.basename(file_path))
                self.arr_qnt.append(self.qnt)

            # Converte a imagem para o formato RGB usando o Pillow (PIL)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_pillow = Image.fromarray(image_rgb)

            # Converte a imagem para um formato que o Tkinter possa exibir
            image_tk = ImageTk.PhotoImage(image_pillow)

            # Atualiza o Label com a nova imagem
            self.image_label.config(image=image_tk)
            self.image_label.image = image_tk  # Mantém uma referência para evitar que a imagem seja destruída pelo coletor de lixo
            self.load_flag = True
            self.resize_image()

    def export_data(self):

        # Variável para guardar o diretório de exportação
        global export_dir

        if not self.arr_images:
            tk.messagebox.showinfo("Alerta", "Nenhuma imagem carregada.")
            return

        # Abre uma caixa de diálogo para escolher o diretório de exportação
        export_dir = filedialog.askdirectory(title="Escolher diretório de exportação")
        
        # Verifica se o usuário selecionou um diretório
        if export_dir:
            # Itera sobre todas as imagens e as exporta para o diretório escolhido
            for i, image in enumerate(self.arr_images):
                arq_name = f"{self.arr_name_images[i]}"  # Nome do arquivo
                arq_path = os.path.join(export_dir, arq_name)
                txtqnt = f'Quantidade total de ovos: {self.arr_qnt[i]}'
                image_copy = cv2.putText(image.copy(), txtqnt, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4)
                cv2.imwrite(arq_path, image_copy)

            tk.messagebox.showinfo("Informação", "Dados exportados com sucesso!")
            self.export_data_flag = True

    def open_destination_folder(self):
        
        if not self.arr_images or not self.export_data_flag:
            # Mostra uma mensagem de alerta se nenhum dado foi exportado ainda
            tk.messagebox.showinfo("Alerta", "Nenhum dado foi exportado ainda. Por favor, exporte os dados primeiro.")
            return

        # Abre a pasta de destino no explorador de arquivos do sistema
        path = os.path.realpath(export_dir)
        os.startfile(path)

    def block_loading_and_update_info(self):
        self.block_loading()
        if self.arr_images:
            self.update_info()
            if self.load_flag:
                # Mensagem de confirmação
                tk.messagebox.showinfo(f"Informação", "Imagens carregadas e contadas com sucesso! \nExporte caso desejar.")
                self.load_flag = False
        
    def load_image_and_update_info(self):
        self.load_image()
        if self.arr_images:
            self.update_info()
            if self.load_flag:
                # Mensagem de confirmação
                tk.messagebox.showinfo(f"Informação", "Imagem carregada e contada com sucesso! \nExporte caso desejar.")
                self.load_flag = False

    def Quit(self): self.root.destroy()

    def About(self): tk.messagebox.showinfo("Informação", "Programa desenvolvido pelo aluno Christian Jonas Oliveira, sob orientação do Prof.: Dr. Jacques Faccon para Avaliação no Trabalho de Conclusão de Curso II")

    def load_logo_image(self):
        # Carregua a imagem usando o Pillow (PIL)
        imagem_original = Image.open('icons/crab.png')
        
        # Redimensione a imagem para a escala desejada (0.4 neste caso)
        new_width = int(imagem_original.width * 4)
        new_height = int(imagem_original.height * 4)
        
        # Use thumbnail() para redimensionar a imagem mantendo a proporção
        imagem_original.thumbnail((new_width, new_height))
        
        # Converte a imagem redimensionada para um formato que o Tkinter possa exibir
        image_tk = ImageTk.PhotoImage(imagem_original)

        # Atualize o self.logo_label com a nova imagem
        self.image_logo_label.config(image=image_tk)
        self.image_logo_label.image = image_tk  # Mantém uma referência para evitar que a imagem seja destruída pelo coletor de lixo



class Application(Functions):
    def __init__(self):
        # Cria a janela principal
        self.root = tk.Tk()
        self.screen()
        self.labels()
        self.Menus()
        self.load_logo_image()
        self.root.bind('<Configure>', self.resize_image)

    def screen(self):
        self.root.title("EggCounter")
        self.root.configure(background='#22353c')
        self.root.geometry("1280x780")  # Tamanho inicial da janela
        self.root.maxsize(width=1920, height=1080)
        self.root.minsize(width=1280, height=780)
        self.root.resizable(True, True)

    def labels(self):
        
        # Cria uma Label para exibir a imagem
        self.image_label = Label(self.root, bd=4, highlightbackground='gray', highlightthickness=3)
        self.image_label.place(relx=0.2, rely=0.02, relwidth=0.79, relheight=0.96)

        #Cria uma Label para exibir a logo
        self.image_logo_label = Label(self.root, bd=4)
        self.image_logo_label.place(relx=0.04, rely=0.8, relwidth=0.10, relheight=0.2)

        # Cria uma  Label para exibir as informações
        self.info_label = Label(self.root, bd=4, highlightbackground='gray', highlightthickness=3)
        self.info_label.place(relx=0.01, rely=0.02, relwidth=0.18, relheight=0.30)

        # Cria uma sublabel para exibir o número de ovos
        self.info_num_label = Label(self.info_label, bd=4, highlightthickness=3, bg = '#FFFFFF', anchor="w")
        self.info_num_label.place(relx=0.01, rely=0.1, relwidth=0.97, relheight=0.3)

        # Cria uma sublabel para exibir o nome da imagem
        self.info_name_label = Label(self.info_label, bd=4, highlightthickness=3, bg = '#FFFFFF', anchor="w")
        self.info_name_label.place(relx=0.01, rely=0.5, relwidth=0.97, relheight=0.3)

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar,  tearoff=0)

        # Adiciona um menu "Arquivo"
        menubar.add_cascade(label = "Arquivo", menu=filemenu)

        # Adiciona itens em cascada no menu "Arquivo"
        filemenu.add_cascade(label="Carregar Imagem", command=self.load_image_and_update_info)
        filemenu.add_cascade(label="Carregar Pasta de Imagens", command=self.block_loading_and_update_info)
        filemenu.add_cascade(label="Exportar Arquivos", command=self.export_data)
        filemenu.add_cascade(label="Pasta de Destino", command=self.open_destination_folder)
        filemenu.add_cascade(label="Sair", command=self.Quit)

        # Adiciona um menu "Sobre"
        menubar.add_cascade(label = "Sobre", command=self.About)
        
if __name__ == "__main__":
    app = Application()
    app.root.mainloop()  # Mova o mainloop para fora da classe Application