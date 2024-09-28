import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pygame

# Inicializar Pygame para manejar sonidos
pygame.mixer.init()

def play_click_sound():
    click_sound = pygame.mixer.Sound("C:/Users/crist/OneDrive/Documentos/Univerisdad 2/intro 2.0/Taller/Proyect_2/Click.mp3")


    click_sound.play()


def play_background_music():
    pygame.mixer.music.load("C://Users//crist//OneDrive//Documentos//Univerisdad 2//intro 2.0/Taller//Proyect_2/Fondo.mp3")  # Cargar Fondo.mp3
    pygame.mixer.music.play(-1)  # Reproducir en bucle


def open_create_window():
    play_click_sound()  # Reproducir el sonido al hacer clic en el botón
    root.destroy()

    create_window = tk.Tk()
    create_window.title("Crear Crucigrama")
    create_window.geometry("800x700")
    create_window.config(bg="Black")
    
    def go_back():
        play_click_sound()
        create_window.destroy()
        open_main_window()

    word_label = tk.Label(create_window, text = "Words", font=("Press Start 2P", 12), fg= "blue", bg="Black")
    word_label.place(x=20, y=100)

    definition_label = tk.Label(create_window, text = "Definition", font=("Press Start 2P", 12, "bold"), fg= "blue", bg="Black")
    definition_label.place(x=20, y=140)

       # Crear entradas al lado derecho de las etiquetas
    word_entry = tk.Entry(create_window, font=("Press Start 2P", 12), fg="White", bg="Black")
    word_entry.place(x=200, y=100)  # Ajusta la posición según sea necesario

    definition_entry = tk.Entry(create_window, font=("Press Start 2P", 12), fg="White", bg="Black")
    definition_entry.place(x=200, y=140)  # Ajusta la posición según sea necesario

    image_path = "C:/Users/Usuario/OneDrive - Estudiantes ITCR/Segundo semestre 2024/Taller de Programación/Proyecto #2/gato.jpeg"  # Cambia esto por la ruta de tu imagen
    img = Image.open(image_path)
    img = img.resize((200, 400), Image.LANCZOS)  
    img_photo = ImageTk.PhotoImage(img)
    image_label = tk.Label(create_window, image=img_photo)
    image_label.image = img_photo  # Mantener una referencia
    image_label.place(x=200, y=200) 
    
    button_back = tk.Button(create_window, text="Devolver", width=10, command=go_back)
    button_back.pack(anchor="ne", padx=10, pady=10)
    
    create_window.mainloop()

def solve_puzzle():
    play_click_sound()
    messagebox.showinfo("Resolver", "Has seleccionado resolver un crucigrama.")

def open_main_window():
    global root
    root = tk.Tk()
    root.title("Crucigrama")
    root.geometry("1525x782+0+0")

    imagen = ImageTk.PhotoImage(Image.open("image.JPG"))
    label = Label(image=imagen)
    label.pack()

    btn = Button(root, text = "Salir", command = quit,background="black",foreground="white",font=("Arial",16,'bold'))
    btn.pack()

    button_create = tk.Button(root, text="Crear",font = ("Arial",16,'bold'), width=15,height=4, command=open_create_window,background = "black",foreground="white")
    button_create.place(x=210, y=500)

    button_solve = tk.Button(root, text="Resolver",font = ("Arial",16,'bold' ), width=15,height=4, command=solve_puzzle,background = "black",foreground="white")
    button_solve.place(x=520, y=500)

    play_background_music()

    root.mainloop()

open_main_window()
