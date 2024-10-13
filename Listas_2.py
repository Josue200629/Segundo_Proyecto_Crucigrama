import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import struct

archivos= []
def listar_archivos_txt(directorio):
    archivos_txt = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.bin')]
    for archivo in archivos_txt:
        archivos.append(archivo)

def get_current_directory():
    return os.path.dirname(os.path.abspath(__file__))

current_directory = get_current_directory()
listar_archivos_txt(current_directory)


class Crucigrama:
    def __init__(self, master):
        self.master = master
        self.master.title("Crucigrama")
        
        # Crear un frame para el crucigrama y uno para las definiciones
        self.frame_crucigrama = tk.Frame(self.master)
        self.frame_crucigrama.grid(row=0, column=1, padx=10, pady=10)
        
        self.frame_definiciones = tk.Frame(self.master)
        self.frame_definiciones.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.tamano_cuadrilatero = (0, 0, 0)  # Dimensiones se inicializan vacías
        self.cuadrilatero = []
        self.botones = []
        self.definiciones = []

        self.archivo_seleccionado = False
        self.listbox= tk.Listbox(self.master)
        self.listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        self.cargar_lista_archivos()

        self.cargar_btn = tk.Button(self.master, text= 'Cargar archivos', command=self.cargar_crucigrama)
        self.cargar_btn.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

        # Pedir al usuario que cargue un crucigrama
        self.cargar_crucigrama()

    def cargar_lista_archivos(self):
        self.listbox.delete(0, tk.END)  # Asegurar que la lista esté vacía antes de llenarla
        for archivo in archivos:
            self.listbox.insert(tk.END, archivo)

    def cargar_crucigrama(self):
        seleccion_indices = self.listbox.curselection()
        if seleccion_indices:
            archivo_seleccionado = self.listbox.get(seleccion_indices)
            self.archivo_seleccionado = archivo_seleccionado
            messagebox.showinfo("Archivo Seleccionado", f"Has seleccionado: {archivo_seleccionado}")
            self.limpiar_ventana()
            self.cargar_crucigrama_especifico(archivo_seleccionado)      
        else:
            self.archivo_seleccionado = False
            messagebox.showwarning("Advertencia", "Selecciona un archivo.")

    def limpiar_ventana(self):
        for widget in self.frame_crucigrama.winfo_children():
            widget.destroy()
        for widget in self.frame_definiciones.winfo_children():
            widget.destroy()

    def cargar_crucigrama_especifico(self, nombre_crucigrama=False):
        if nombre_crucigrama:
            # Intentar cargar el archivo binario
            if os.path.exists(nombre_crucigrama):
                with open(nombre_crucigrama, 'rb') as archivo:
                    try:
                        self.leer_archivo_crucigrama(archivo)
                        self.crear_interfaz_crucigrama()
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo leer el archivo binario: {e}")
            else:
                messagebox.showerror("Error", "El archivo de crucigrama no existe.")
        else:
            messagebox.showerror("Error", "Nombre no ingresado.")

    def leer_archivo_crucigrama(self, archivo):
        try:
            version = struct.unpack('B', archivo.read(1))[0]
            print(f"Versión: {version}")

            self.tamano_cuadrilatero = struct.unpack('3i', archivo.read(12))
            print(f"Dimensiones: {self.tamano_cuadrilatero}")

            self.cuadrilatero = [['' for _ in range(self.tamano_cuadrilatero[1])] for _ in range(self.tamano_cuadrilatero[0])]
            
            num_palabras = struct.unpack('I', archivo.read(4))[0]
            print(f"Número de palabras: {num_palabras}")

            palabras_info = []
            for _ in range(num_palabras):
                longitud_palabra = struct.unpack('B', archivo.read(1))[0]
                palabra = archivo.read(longitud_palabra).decode('utf-8')
                print(f"Palabra: {palabra}")

                longitud_definicion = struct.unpack('H', archivo.read(2))[0]
                definicion = archivo.read(longitud_definicion).decode('utf-8')
                print(f"Definición: {definicion}")

                posicion = struct.unpack('3i', archivo.read(12))
                direccion = struct.unpack('B', archivo.read(1))[0]

                palabras_info.append((palabra, definicion, posicion, direccion))

            self.cargar_palabras(palabras_info)
        except Exception as e:
            print(f"Error al leer el archivo de crucigrama: {e}")

    def cargar_palabras(self, palabras_info):
        for idx, (palabra, definicion, posicion, direccion) in enumerate(palabras_info, start=1):
            x, y, _ = posicion
            if direccion == 0:  # Horizontal
                for j, letra in enumerate(palabra):
                    if 0 <= x < self.tamano_cuadrilatero[0] and 0 <= y + j < self.tamano_cuadrilatero[1]:
                        self.cuadrilatero[x][y + j] = letra
            elif direccion == 1:  # Vertical
                for i, letra in enumerate(palabra):
                    if 0 <= x + i < self.tamano_cuadrilatero[0] and 0 <= y < self.tamano_cuadrilatero[1]:
                        self.cuadrilatero[x + i][y] = letra
            
            self.definiciones.append(f"{idx}. {definicion}")

    def crear_interfaz_crucigrama(self):
        for widget in self.frame_crucigrama.winfo_children():
            widget.destroy()
        
        ancho_ventana = self.tamano_cuadrilatero[1] * 35
        alto_ventana = self.tamano_cuadrilatero[0] * 35
        self.master.geometry(f"{ancho_ventana+200}x{alto_ventana+100}")

        # Crear los botones solo para las celdas con letras
        self.botones = []
        for i in range(self.tamano_cuadrilatero[0]):
            fila_botones = []
            for j in range(self.tamano_cuadrilatero[1]):
                letra = self.cuadrilatero[i][j]
                
                if letra:
                    boton = tk.Button(self.frame_crucigrama, text="", width=2, height=1)
                    boton.grid(row=i, column=j, padx=0, pady=0)
                    boton.config(command=lambda i=i, j=j: self.verificar_letra(i, j))
                    boton.letra_correcta = letra
                    fila_botones.append(boton)
                else:
                    fila_botones.append(None)  # Ningún botón si no hay letra

            self.botones.append(fila_botones)
        
        self.mostrar_definiciones()

    def mostrar_definiciones(self):
        for widget in self.frame_definiciones.winfo_children():
            widget.destroy()

        lista_definiciones = tk.Listbox(self.frame_definiciones, height=20, width=40)
        for definicion in self.definiciones:
            lista_definiciones.insert(tk.END, definicion)
        lista_definiciones.pack()

    def verificar_letra(self, i, j):
        boton = self.botones[i][j]
        letra_ingresada = simpledialog.askstring("Letra", "Ingrese una letra:")

        if letra_ingresada:
            letra_ingresada = letra_ingresada.upper()
            if letra_ingresada == boton.letra_correcta:
                boton.config(text=letra_ingresada, bg="green")
            else:
                boton.config(text="", bg="red")

root = tk.Tk()
crucigrama = Crucigrama(root)
root.mainloop()
