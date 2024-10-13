import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import pickle

class Crucigrama:
    def __init__(self, master):
        self.master = master
        self.master.title("Crucigrama")
        self.master.geometry("500x500")

        self.tamano_cuadrilatero = 10
        self.cuadrilatero = [['' for _ in range(self.tamano_cuadrilatero)] for _ in range(self.tamano_cuadrilatero)]

        # Crear los botones para representar cada celda del cuadrilátero
        self.botones = []
        for i in range(self.tamano_cuadrilatero):
            fila_botones = []
            for j in range(self.tamano_cuadrilatero):
                boton = tk.Button(self.master, text="", width=5, height=2, 
                                  command=lambda i=i, j=j: self.ingresar_letra(i, j))
                boton.grid(row=i, column=j)
                fila_botones.append(boton)
            self.botones.append(fila_botones)

        # Pedir al usuario que cargue un crucigrama
        self.cargar_crucigrama()

    def cargar_crucigrama(self):
        # Pedir al usuario que ingrese el nombre del crucigrama
        nombre_crucigrama = simpledialog.askstring("Cargar crucigrama", "Ingrese el nombre del crucigrama:")
        
        if nombre_crucigrama:
            archivo_txt = f"{nombre_crucigrama}.txt"
            archivo_bin = f"{nombre_crucigrama}.bin"
            
            # Verificar si el archivo de texto existe
            if os.path.exists(archivo_txt):
                # Intentar cargar el archivo binario
                if os.path.exists(archivo_bin):
                    with open(archivo_bin, 'rb') as archivo:
                        try:
                            palabras_binarias = pickle.load(archivo)
                            self.cargar_palabras(palabras_binarias)
                        except Exception as e:
                            messagebox.showerror("Error", f"No se pudo leer el archivo binario: {e}")
                else:
                    # Si el archivo binario no existe, leer el archivo de texto y crear el binario
                    with open(archivo_txt, 'r') as archivo:
                        palabras = archivo.readlines()
                        palabras = [palabra.strip().upper() for palabra in palabras if palabra.strip().isalpha()]

                    # Guardar las palabras en formato binario
                    with open(archivo_bin, 'wb') as archivo:
                        pickle.dump(palabras, archivo)

                    # Cargar las palabras en el tablero
                    self.cargar_palabras(palabras)
            else:
                messagebox.showerror("Error", "El archivo de crucigrama no existe.")
    
    def cargar_palabras(self, palabras):
        """Coloca las palabras leídas del archivo binario en el tablero de forma aleatoria."""
        for idx, palabra in enumerate(palabras):
            if idx < self.tamano_cuadrilatero:
                for j, letra in enumerate(palabra):
                    if j < self.tamano_cuadrilatero:
                        self.cuadrilatero[idx][j] = letra
                        self.botones[idx][j].config(text=letra, state=tk.DISABLED)

    def ingresar_letra(self, i, j):
        if self.cuadrilatero[i][j]:  # Si la celda ya tiene una letra, no permitir sobreescribirla
            return
        
        nueva_palabra = simpledialog.askstring("Nueva palabra", "Ingrese una nueva palabra:")
        
        if nueva_palabra and nueva_palabra.isalpha():
            nueva_palabra = nueva_palabra.upper()
            coincidencia_encontrada = False
            
            for idx_nueva, letra_nueva in enumerate(nueva_palabra):
                for fila in range(self.tamano_cuadrilatero):
                    for col in range(self.tamano_cuadrilatero):
                        if self.cuadrilatero[fila][col] == letra_nueva:
                            coincidencia_encontrada = True
                            if self.agregar_palabra_vertical(nueva_palabra, idx_nueva, fila, col) or self.agregar_palabra_horizontal(nueva_palabra, idx_nueva, fila, col):
                                return

            if not coincidencia_encontrada:
                print("No se encontró coincidencia para insertar la palabra.")

    def agregar_palabra_vertical(self, palabra, idx_letra, fila, col):
        inicio_fila = fila - idx_letra
        if inicio_fila < 0 or inicio_fila + len(palabra) > self.tamano_cuadrilatero:
            return False

        for i in range(len(palabra)):
            if self.cuadrilatero[inicio_fila + i][col] not in ('', palabra[i]):
                return False

        for i in range(len(palabra)):
            self.cuadrilatero[inicio_fila + i][col] = palabra[i]
            self.botones[inicio_fila + i][col].config(text=palabra[i], state=tk.DISABLED)

        return True

    def agregar_palabra_horizontal(self, palabra, idx_letra, fila, col):
        inicio_col = col - idx_letra
        if inicio_col < 0 or inicio_col + len(palabra) > self.tamano_cuadrilatero:
            return False

        for j in range(len(palabra)):
            if self.cuadrilatero[fila][inicio_col + j] not in ('', palabra[j]):
                return False

        for j in range(len(palabra)):
            self.cuadrilatero[fila][inicio_col + j] = palabra[j]
            self.botones[fila][inicio_col + j].config(text=palabra[j], state=tk.DISABLED)

        return True

root = tk.Tk()
crucigrama = Crucigrama(root)
root.mainloop()
