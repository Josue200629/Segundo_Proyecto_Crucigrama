import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pygame
import os
import struct

def get_current_directory():
    """Obtiene el directorio actual del archivo en ejecución."""
    return os.path.dirname(os.path.abspath(__file__))

# Obtener el directorio actual
current_directory = get_current_directory()

# Inicializar Pygame para manejar sonidos
pygame.mixer.init()
datos = ()  # tupla para almacenar datos

def play_click_sound():
    """Reproduce un sonido de clic al interactuar con la interfaz."""
    click_sound = pygame.mixer.Sound(f"{current_directory}/Click.mp3")
    click_sound.play()

def play_background_music():
    """Carga y reproduce música de fondo en bucle."""
    pygame.mixer.music.load(f"{current_directory}/Fondo.mp3")  # Cargar Fondo.mp3
    pygame.mixer.music.play(-1)  # Reproducir en bucle

def open_create_window():
    """Abre una nueva ventana para crear un crucigrama."""
    cont = 0  # Contador para el tamaño
    current_size = None  # Tamaño actual (inicialmente indefinido)
    list_words = []  # Lista para almacenar palabras
    list_definitions = []  # Lista para almacenar definiciones
    Version = 1  # Versión inicial

    play_click_sound()  # Reproducir el sonido al hacer clic en el botón
    root.destroy()  # Cerrar la ventana principal

    # Crear nueva ventana para el crucigrama
    create_window = tk.Tk()
    create_window.title("Crear Crucigrama")
    create_window.geometry("1525x782+0+0")
    create_window.config(bg="Black")

    def clear_screen():
        """Elimina todos los widgets de la ventana excepto la imagen."""
        for widget in create_window.winfo_children():
            if widget != label:  # Mantener la imagen
                widget.destroy()  # Eliminar el widget

    def toggle_size(button):
        """Alterna entre diferentes tamaños de crucigrama."""
        nonlocal cont
        global current_sizex, current_sizey, current_sizez
        sizes = [5, 10, 15]  # Tamaños disponibles
        button.config(text=str(sizes[cont]))  # Actualizar texto del botón
        if button == button_sizex:
            current_sizex = sizes[cont]  # Guardar tamaño actual
        elif button == button_sizey:
            current_sizey = sizes[cont]
        elif button == button_sizez:
            current_sizez = sizes[cont]
        cont += 1  # Incrementar contador
        if cont == len(sizes):
            cont = 0  # Reiniciar contador si se alcanzó el final

    def palabra_a_binario(palabra):
        binario = ''.join(format(ord(c), '08b') for c in palabra)
        return binario
    
    def start():
        datos.append(struct.pack('I', len(list_words)))
        for i in range(len(list_words)):
            datos.append(struct.pack('B', len(list_words[i])))
            datos.append(palabra_a_binario(list_words[i]))
            datos.append(struct.pack('H', len(list_definitions[i])))
            datos.append(palabra_a_binario(list_definitions[i]))
            if dimension == 'Horizontal':
                datos.append(struct.pack('B', 0))
            if dimension == 'Vertical':
                datos.append(struct.pack('B', 1))
            if dimension == 'Profundidad':
                datos.append(struct.pack('B', 2))

    def go_back():
        """Regresa a la ventana principal y limpia los datos."""
        list_words.clear()  # Limpiar lista de palabras
        list_definitions.clear()  # Limpiar lista de definiciones
        datos.clear()  # Limpiar datos
        play_click_sound()  # Reproducir sonido al hacer clic
        create_window.destroy()  # Cerrar ventana de creación
        open_main_window()  # Abrir ventana principal
    
    # Cargar y mostrar la imagen en la ventana
    imagen = ImageTk.PhotoImage(Image.open("image1.JPG"))
    label = tk.Label(create_window, image=imagen)
    label.pack() 

    def save_size():
        try:
            """Guarda el tamaño seleccionado en la lista de datos."""
            nonlocal cont
            datos.append(struct.pack('B', Version))  # Agregar versión en formato binario (1 byte)
            datos.append(struct.pack('i', current_sizex))  # Agregar tamaño X en formato binario (4 bytes)
            datos.append(struct.pack('i', current_sizey))  # Agregar tamaño Y en formato binario (4 bytes)
            datos.append(struct.pack('i', current_sizez))  
            cont = 0  # Reiniciar contador
            words()  # Llamar a la función words (no definida en el fragmento)
        except NameError:
            messagebox.showerror("Error", "Tamaño indefinido")
            
    def salve():
        """Guarda una palabra y su definición, y habilita el botón para comenzar el juego si se cumplen las condiciones."""
        word = word_entry.get()  # Obtener la palabra del campo de entrada
        definition = definition_entry.get()  # Obtener la definición del campo de entrada
        
        # Validar la entrada de la palabra y la definición
        if word == "" or definition == "":
            messagebox.showerror("Error", "Ingrese una palabra y una definición")  # Mostrar error si la palabra o definición son inválidas
            return 
        elif word.upper in list_words:
            messagebox.showerror("Error", "Palabra ya ingresada")  # Mostrar error si la palabra ya existe
            return
        elif len(word)> current_sizex and len(word) >current_sizey and len(word) > current_sizez:
            messagebox.showerror('Error:', "Palabra muy extensa")
            return
        # Habilitar el botón para comenzar si se han ingresado al menos 2 palabras
        if len(list_words) >= 2:
            button_start = tk.Button(create_window, text="Comenzar", font=("Press Start 2P", 12, "bold"), bg="Black", fg="Blue", command=start)
            button_start.place(x=500, y=250)
        
        # Agregar la palabra y su definición a las listas correspondientes
        list_words.append(word.upper)  # Guardar en formato diccionario
        list_definitions.append(definition)  # Agregar la definición a la lista
        messagebox.showinfo("Append", "Palabra y definición agregados..")  # Mensaje de éxito
        definition_entry.delete(0, 'end')  # Limpiar el campo de definición
        word_entry.delete(0, 'end')  # Limpiar el campo de palabra

    # Crear botones para la ventana de creación
    button_sizex = tk.Button(create_window, text="Tamaño X", font=("Press Start 2P", 25, "bold"), bg="Black", fg="Blue", command=lambda:toggle_size(button_sizex))
    button_sizex.place(x=100, y=250)

    button_sizey = tk.Button(create_window, text="Tamaño Y", font=("Press Start 2P", 25, "bold"), bg="Black", fg="Blue", command=lambda:toggle_size(button_sizey))
    button_sizey.place(x=500, y=250)
    
    button_sizez = tk.Button(create_window, text="Tamaño Z", font=("Press Start 2P", 25, "bold"), bg="Black", fg="Blue", command=lambda:toggle_size(button_sizez))
    button_sizez.place(x=900, y=250)

    button_save = tk.Button(create_window, text="Guardar Tamaño", font=("Press Start 2P", 15, "bold"), bg="Black", fg="Blue", command=save_size)
    button_save.place(x=500, y=400)
    
    def words():
        """Configura la interfaz para ingresar palabras y definiciones."""
        global word_entry, definition_entry  # Variables globales para los campos de entrada
        def toggle_dimensions():
            """Alterna entre las dimensiones (horizontal, vertical, profundidad)."""
            nonlocal cont  # Usar el contador local
            global dimension  # Variable global para la dimensión actual
            dimensions = ["Horizontal", "Vertical", "Profundidad"]  # Opciones de dimensión
            dimension_size.config(text=dimensions[cont])  # Actualizar el texto del botón de dimensión
            dimension = dimensions[cont]  # Guardar la dimensión actual
            if cont == 2:
                cont = 0  # Reiniciar el contador si se ha alcanzado el final
            cont += 1  # Incrementar el contador

        clear_screen()  # Limpiar la pantalla antes de mostrar nuevos widgets
        button_back = tk.Button(create_window, text="Devolver", font=("Press Start 2P", 10, "bold"), width=10, command=go_back)
        button_back.place(x=70, y=200)

        # Botón para seleccionar la dimensión
        dimension_size = tk.Button(create_window, text="Dirección", font=("Press Start 2P", 10, "bold"), command=toggle_dimensions)
        dimension_size.place(x=500, y=200)

        # Botón para guardar la palabra y la definición
        button_salve = tk.Button(create_window, text="Guardar", font=("Press Start 2P", 10, "bold"), width=10, command=salve)
        button_salve.place(x=290, y=200)

        # Etiquetas y campos de entrada para la palabra y definición
        word_label = tk.Label(create_window, text="Words", font=("Press Start 2P", 12), fg="blue", bg="Black")
        word_label.place(x=70, y=100)

        definition_label = tk.Label(create_window, text="Definition", font=("Press Start 2P", 12, "bold"), fg="blue", bg="Black")
        definition_label.place(x=70, y=140)

        word_entry = tk.Entry(create_window, font=("Press Start 2P", 12), fg="White", bg="Black")
        word_entry.place(x=290, y=100)  

        definition_entry = tk.Entry(create_window, font=("Press Start 2P", 12), fg="White", bg="Black")
        definition_entry.place(x=290, y=140)  

    # Iniciar el bucle principal de la ventana de creación
    create_window.mainloop()

def solve_puzzle():
    """Función para resolver el crucigrama."""
    play_click_sound()  # Reproducir sonido al seleccionar resolver
    messagebox.showinfo("Resolver", "Has seleccionado resolver un crucigrama.")  # Mensaje de información

def open_main_window():
    """Abre la ventana principal de la aplicación."""
    global root  # Variable global para la ventana principal
    root = tk.Tk()
    root.title("Crucigrama")
    root.geometry("1525x782+0+0")

    # Cargar y mostrar imagen en la ventana principal
    imagen = ImageTk.PhotoImage(Image.open("image.JPG"))
    label = tk.Label(image=imagen)
    label.pack()

    # Botón para crear un nuevo crucigrama
    button_create = tk.Button(root, text="Crear", font=("Press Start 2P", 16, 'bold'), width=12, height=4, command=open_create_window, background="black", foreground="white")
    button_create.place(x=200, y=500)

    # Botón para resolver un crucigrama
    button_solve = tk.Button(root, text="Resolver", font=("Press Start 2P", 16, 'bold'), width=12, height=4, command=solve_puzzle, background="black", foreground="white")
    button_solve.place(x=510, y=500)

    play_background_music()  # Iniciar la música de fondo

    # Iniciar el bucle principal de la ventana
    root.mainloop()

# Abrir la ventana principal
open_main_window()
