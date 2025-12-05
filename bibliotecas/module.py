import tkinter as tk
from tkinter import messagebox
import random


class MenuConfiguracion:
    
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Buscaminas - Configuración")
        self.ventana.geometry("400x500")
        self.ventana.resizable(False, False)
        
        self.filas = tk.IntVar(value=10)
        self.columnas = tk.IntVar(value=10)
        self.minas = tk.IntVar(value=15)
        
        self.crear_menu()
    
    def crear_menu(self):
        titulo = tk.Label(
            self.ventana,
            text="🎮 BUSCAMINAS 🎮",
            font=('Arial', 24, 'bold'),
            fg='darkblue'
        )
        titulo.pack(pady=20)
        
        frame_dificultad = tk.LabelFrame(
            self.ventana,
            text="Dificultad Predefinida",
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10
        )
        frame_dificultad.pack(pady=10, padx=20, fill='x')
        
        tk.Button(
            frame_dificultad,
            text="🟢 Fácil (8x8, 10 minas)",
            command=lambda: self.establecer_dificultad(8, 8, 10),
            font=('Arial', 11),
            bg='lightgreen',
            width=25
        ).pack(pady=5)
        
        tk.Button(
            frame_dificultad,
            text="🟡 Medio (10x10, 15 minas)",
            command=lambda: self.establecer_dificultad(10, 10, 15),
            font=('Arial', 11),
            bg='lightyellow',
            width=25
        ).pack(pady=5)
        
        tk.Button(
            frame_dificultad,
            text="🔴 Difícil (15x15, 35 minas)",
            command=lambda: self.establecer_dificultad(15, 15, 35),
            font=('Arial', 11),
            bg='lightcoral',
            width=25
        ).pack(pady=5)
        
        tk.Button(
            frame_dificultad,
            text="⚫ Experto (20x20, 70 minas)",
            command=lambda: self.establecer_dificultad(20, 20, 70),
            font=('Arial', 11),
            bg='lightgray',
            width=25
        ).pack(pady=5)
        
        frame_custom = tk.LabelFrame(
            self.ventana,
            text="Personalizado",
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10
        )
        frame_custom.pack(pady=10, padx=20, fill='x')
        
        tk.Label(frame_custom, text="Filas:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        tk.Spinbox(
            frame_custom,
            from_=5,
            to=30,
            textvariable=self.filas,
            width=10,
            font=('Arial', 10)
        ).grid(row=0, column=1, pady=5)
        
        tk.Label(frame_custom, text="Columnas:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        tk.Spinbox(
            frame_custom,
            from_=5,
            to=30,
            textvariable=self.columnas,
            width=10,
            font=('Arial', 10)
        ).grid(row=1, column=1, pady=5)
        
        tk.Label(frame_custom, text="Minas:", font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        tk.Spinbox(
            frame_custom,
            from_=1,
            to=200,
            textvariable=self.minas,
            width=10,
            font=('Arial', 10)
        ).grid(row=2, column=1, pady=5)
        
        tk.Button(
            frame_custom,
            text="🎯 Jugar Personalizado",
            command=self.iniciar_juego,
            font=('Arial', 10, 'bold'),
            bg='lightblue',
            width=25
        ).grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Button(
            self.ventana,
            text="▶️ JUGAR",
            command=self.iniciar_juego,
            font=('Arial', 14, 'bold'),
            bg='lightblue',
            width=20,
            height=2
        ).pack(pady=20)
    
    def establecer_dificultad(self, filas, columnas, minas):
        self.filas.set(filas)
        self.columnas.set(columnas)
        self.minas.set(minas)
    
    def iniciar_juego(self):
        filas = self.filas.get()
        columnas = self.columnas.get()
        minas = self.minas.get()
        
        if minas >= filas * columnas:
            messagebox.showerror("Error", "¡Demasiadas minas! Debe haber al menos una casilla sin mina.")
            return
        
        self.ventana.destroy()
        juego = Buscaminas(filas, columnas, minas)
        juego.iniciar()
    
    def mostrar(self):
        self.ventana.mainloop()


class Buscaminas:
    
    def __init__(self, filas=10, columnas=10, minas=15):
        self.filas = filas
        self.columnas = columnas
        self.num_minas = minas
        self.juego_terminado = False
        self.primer_click = True
        
        self.ventana = tk.Tk()
        self.ventana.title("Buscaminas")
        
        tamaño_boton = max(2, min(4, 40 // max(filas, columnas)))
        self.tamaño_boton = tamaño_boton
        
        tamaño_fuente = max(8, min(14, 120 // max(filas, columnas)))
        self.tamaño_fuente = tamaño_fuente
        
        self.tablero = [[0 for _ in range(columnas)] for _ in range(filas)]
        self.revelado = [[False for _ in range(columnas)] for _ in range(filas)]
        self.banderas = [[False for _ in range(columnas)] for _ in range(filas)]
        self.botones = [[None for _ in range(columnas)] for _ in range(filas)]
        
        self.crear_interfaz()
    
    def colocar_minas(self, fila_segura, col_segura):
        minas_colocadas = 0
        while minas_colocadas < self.num_minas:
            fila = random.randint(0, self.filas - 1)
            col = random.randint(0, self.columnas - 1)
            
            es_zona_segura = abs(fila - fila_segura) <= 1 and abs(col - col_segura) <= 1
            
            if self.tablero[fila][col] != -1 and not es_zona_segura:
                self.tablero[fila][col] = -1
                minas_colocadas += 1
    
    def calcular_numeros(self):
        for fila in range(self.filas):
            for col in range(self.columnas):
                if self.tablero[fila][col] == -1:
                    continue
                
                minas_adyacentes = 0
                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if df == 0 and dc == 0:
                            continue
                        
                        nueva_fila = fila + df
                        nueva_col = col + dc
                        
                        if 0 <= nueva_fila < self.filas and 0 <= nueva_col < self.columnas:
                            if self.tablero[nueva_fila][nueva_col] == -1:
                                minas_adyacentes += 1
                
                self.tablero[fila][col] = minas_adyacentes
    
    def crear_interfaz(self):
        info_frame = tk.Frame(self.ventana, bg='lightgray')
        info_frame.pack(pady=5, padx=10, fill='x')
        
        tk.Label(
            info_frame,
            text=f"💣 Minas: {self.num_minas}",
            font=('Arial', self.tamaño_fuente, 'bold'),
            bg='lightgray'
        ).pack(side='left', padx=10)
        
        tk.Label(
            info_frame,
            text=f"📏 {self.filas}x{self.columnas}",
            font=('Arial', self.tamaño_fuente, 'bold'),
            bg='lightgray'
        ).pack(side='right', padx=10)
        
        frame = tk.Frame(self.ventana)
        frame.pack(padx=10, pady=10)
        
        for fila in range(self.filas):
            for col in range(self.columnas):
                boton = tk.Button(
                    frame,
                    width=self.tamaño_boton,
                    height=self.tamaño_boton // 2,
                    font=('Arial', self.tamaño_fuente, 'bold'),
                    bg='lightgray'
                )
                boton.grid(row=fila, column=col, padx=1, pady=1)
                
                boton.bind('<Button-1>', lambda e, f=fila, c=col: self.revelar_casilla(f, c))
                boton.bind('<Button-3>', lambda e, f=fila, c=col: self.alternar_bandera(f, c))
                
                self.botones[fila][col] = boton
        
        boton_reiniciar = tk.Button(
            self.ventana,
            text="🔄 Reiniciar",
            command=self.reiniciar_juego,
            font=('Arial', self.tamaño_fuente, 'bold'),
            bg='lightblue',
            padx=15,
            pady=5
        )
        boton_reiniciar.pack(pady=5)
        
        boton_menu = tk.Button(
            self.ventana,
            text="⚙️ Cambiar Dificultad",
            command=self.volver_menu,
            font=('Arial', self.tamaño_fuente, 'bold'),
            bg='lightyellow',
            padx=15,
            pady=5
        )
        boton_menu.pack(pady=5)
    
    def revelar_casilla(self, fila, col):
        if self.juego_terminado or self.banderas[fila][col] or self.revelado[fila][col]:
            return
        
        if self.primer_click:
            self.primer_click = False
            self.colocar_minas(fila, col)
            self.calcular_numeros()
        
        self.revelado[fila][col] = True
        
        if self.tablero[fila][col] == -1:
            self.botones[fila][col].config(text='💣', bg='red')
            self.terminar_juego(False)
            return
        
        numero = self.tablero[fila][col]
        
        colores = {
            0: 'white', 1: 'blue', 2: 'green', 3: 'red',
            4: 'darkblue', 5: 'darkred', 6: 'cyan', 7: 'black', 8: 'gray'
        }
        
        if numero == 0:
            self.botones[fila][col].config(text='', bg='white', relief=tk.SUNKEN)
            self.revelar_adyacentes(fila, col)
        else:
            self.botones[fila][col].config(
                text=str(numero),
                fg=colores.get(numero, 'black'),
                bg='white',
                relief=tk.SUNKEN
            )
        
        self.verificar_victoria()
    
    def revelar_adyacentes(self, fila, col):
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if df == 0 and dc == 0:
                    continue
                
                nueva_fila = fila + df
                nueva_col = col + dc
                
                if (0 <= nueva_fila < self.filas and 
                    0 <= nueva_col < self.columnas and 
                    not self.revelado[nueva_fila][nueva_col] and
                    not self.banderas[nueva_fila][nueva_col]):
                    
                    self.revelar_casilla(nueva_fila, nueva_col)
    
    def alternar_bandera(self, fila, col):
        if self.revelado[fila][col] or self.juego_terminado:
            return
        
        self.banderas[fila][col] = not self.banderas[fila][col]
        
        if self.banderas[fila][col]:
            self.botones[fila][col].config(text='🚩', fg='red')
        else:
            self.botones[fila][col].config(text='', fg='black')
    
    def verificar_victoria(self):
        casillas_sin_revelar = 0
        for fila in range(self.filas):
            for col in range(self.columnas):
                if not self.revelado[fila][col] and self.tablero[fila][col] != -1:
                    casillas_sin_revelar += 1
        
        if casillas_sin_revelar == 0:
            self.terminar_juego(True)
    
    def terminar_juego(self, victoria):
        self.juego_terminado = True
        
        for fila in range(self.filas):
            for col in range(self.columnas):
                if self.tablero[fila][col] == -1:
                    if victoria:
                        self.botones[fila][col].config(text='💣', bg='lightgreen')
                    else:
                        if not self.revelado[fila][col]:
                            self.botones[fila][col].config(text='💣', bg='orange')
        
        if victoria:
            messagebox.showinfo("¡Victoria!", "¡Felicidades! Has ganado el juego.")
        else:
            messagebox.showinfo("Derrota", "¡Boom! Has perdido. Inténtalo de nuevo.")
    
    def reiniciar_juego(self):
        self.ventana.destroy()
        nuevo_juego = Buscaminas(self.filas, self.columnas, self.num_minas)
        nuevo_juego.iniciar()
    
    def volver_menu(self):
        self.ventana.destroy()
        menu = MenuConfiguracion()
        menu.mostrar()
    
    def iniciar(self):
        self.ventana.mainloop()