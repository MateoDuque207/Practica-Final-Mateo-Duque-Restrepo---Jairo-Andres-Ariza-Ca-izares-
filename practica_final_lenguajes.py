import tkinter as tk
from tkinter import messagebox

# Clase para dividir la cadena FEN
class AnalizadorLexico:
    def __init__(self, cadena):
        self.cadena = cadena
        self.partes = []
        self.errores = []
    
    def analizar(self):
        # Dividir por espacios
        self.partes = self.cadena.split(' ')
        
        # Verificar que tenga 6 partes
        if len(self.partes) != 6:
            self.errores.append(f"Error: debe tener 6 campos separados por espacios (tiene {len(self.partes)})")
            return False
        
        return True


# Clase para verificar que la cadena sea valida
class AnalizadorSintactico:
    def __init__(self, partes):
        self.tablero_str = partes[0]
        self.turno = partes[1]
        self.enroque = partes[2]
        self.en_passant = partes[3]
        self.medio_mov = partes[4]
        self.mov_completo = partes[5]
        
        self.tablero = []
        self.errores = []
    
    def validar(self):
        # Validar cada parte
        if not self.validar_tablero():
            return False
        if not self.validar_turno():
            return False
        if not self.validar_enroque():
            return False
        if not self.validar_en_passant():
            return False
        if not self.validar_contadores():
            return False
        
        return True
    
    def validar_tablero(self):
        # Separar las filas
        filas = self.tablero_str.split('/')
        
        # Debe haber 8 filas
        if len(filas) != 8:
            self.errores.append(f"Error: el tablero debe tener 8 filas (tiene {len(filas)})")
            return False
        
        # Procesar cada fila
        for i in range(8):
            fila = []
            casillas = 0
            
            for c in filas[i]:
                # Si es numero, son casillas vacias
                if c.isdigit():
                    n = int(c)
                    if n < 1 or n > 8:
                        self.errores.append(f"Error fila {i+1}: numero invalido '{c}'")
                        return False
                    casillas += n
                    for j in range(n):
                        fila.append(' ')
                
                # Si es letra, es una pieza
                elif c in 'pnbrqkPNBRQK':
                    casillas += 1
                    fila.append(c)
                
                # Si no es ni numero ni pieza valida
                else:
                    self.errores.append(f"Error fila {i+1}: caracter invalido '{c}'")
                    return False
            
            # Verificar que la fila tenga 8 casillas
            if casillas != 8:
                self.errores.append(f"Error fila {i+1}: tiene {casillas} casillas (debe tener 8)")
                return False
            
            self.tablero.append(fila)
        
        return True
    
    def validar_turno(self):
        # Solo puede ser w o b
        if self.turno != 'w' and self.turno != 'b':
            self.errores.append(f"Error turno: '{self.turno}' debe ser 'w' o 'b'")
            return False
        return True
    
    def validar_enroque(self):
        # Puede ser - o combinacion de KQkq
        if self.enroque == '-':
            return True
        
        # Verificar caracteres validos
        for c in self.enroque:
            if c not in 'KQkq':
                self.errores.append(f"Error enroque: '{c}' no es valido")
                return False
        
        return True
    
    def validar_en_passant(self):
        # Puede ser - o casilla tipo e3
        if self.en_passant == '-':
            return True
        
        # Debe tener 2 caracteres
        if len(self.en_passant) != 2:
            self.errores.append(f"Error en passant: '{self.en_passant}' formato invalido")
            return False
        
        # Primera letra debe ser a-h
        if self.en_passant[0] not in 'abcdefgh':
            self.errores.append(f"Error en passant: '{self.en_passant[0]}' debe ser a-h")
            return False
        
        # Segundo caracter debe ser 3 o 6
        if self.en_passant[1] not in '36':
            self.errores.append(f"Error en passant: '{self.en_passant[1]}' debe ser 3 o 6")
            return False
        
        return True
    
    def validar_contadores(self):
        # Verificar que sean numeros
        if not self.medio_mov.isdigit():
            self.errores.append(f"Error: medio movimiento debe ser numero")
            return False
        
        if not self.mov_completo.isdigit():
            self.errores.append(f"Error: movimiento completo debe ser numero")
            return False
        
        # El movimiento completo debe ser mayor a 0
        if int(self.mov_completo) < 1:
            self.errores.append(f"Error: movimiento completo debe ser >= 1")
            return False
        
        return True


# Ventana grafica
class Ventana:
    def __init__(self, root):
        self.root = root
        self.root.title("Parser FEN - Ajedrez")
        self.root.geometry("700x750")
        self.root.configure(bg='#1e1e2f')
        
        # Piezas en unicode (creamos un diccionario con las piezas y sus simbolos)
        self.piezas = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        }
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Titulo
        titulo = tk.Label(self.root, text="Parser FEN", font=('Segoe UI', 24, 'bold'), bg='#1e1e2f', fg='#e0b973')
        titulo.pack(pady=15)
        
        # Instrucciones
        inst = tk.Label(self.root, text="Ingrese una cadena FEN:", font=('Segoe UI', 12), bg='#1e1e2f', fg='#dcdcdc')
        inst.pack(pady=5)
        
        # Caja de texto
        self.entrada = tk.Entry(self.root, width=60, font=('Trebuchet MS', 10))
        self.entrada.pack(pady=10)
        
        # Ejemplo inicial (el tablero inicial basicamente)
        ejemplo = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.entrada.insert(0, ejemplo)
        
        # Boton
        boton = tk.Button(self.root, text="Analizar", command=self.analizar, font=('Trebuchet MS', 12), bg='#27ae60', fg='white', padx=20, pady=8)
        boton.pack(pady=10)
        
        # Area del tablero
        self.area_tablero = tk.Frame(self.root, bg='#1e1e2f')
        self.area_tablero.pack(pady=15)
        
        # Mensaje
        self.mensaje = tk.Label(self.root, text="", font=('Segoe UI', 12, 'italic'), bg='#1e1e2f', fg='#dcdcdc')

        self.mensaje.pack(pady=10)
    
    def analizar(self):
        cadena = self.entrada.get()
        
        if not cadena:
            messagebox.showwarning("Advertencia", "Ingrese una cadena FEN")
            return
        
        # Limpiar tablero anterior
        for widget in self.area_tablero.winfo_children():
            widget.destroy()
        
        # Analisis lexico
        lexico = AnalizadorLexico(cadena)
        if not lexico.analizar():
            self.mostrar_error(lexico.errores)
            return
        
        # Analisis sintactico
        sintactico = AnalizadorSintactico(lexico.partes)
        if not sintactico.validar():
            self.mostrar_error(sintactico.errores)
            return
        
        # Si todo esta bien, dibujar
        self.dibujar_tablero(sintactico.tablero)
        
        # Mensaje de exito
        turno_texto = "Blancas" if sintactico.turno == 'w' else "Negras"
        self.mensaje.config(text=f"FEN valido - Turno: {turno_texto}", fg='#2ecc71')
    
    def dibujar_tablero(self, tablero):
        # Dibujar cada casilla
        for fila in range(8):
            for col in range(8):
                # Color de la casilla
                if (fila + col) % 2 == 0:
                    color = '#f5deb3'
                else:
                    color = '#8b5a2b'
                
                # Obtener pieza
                pieza = tablero[fila][col]
                simbolo = self.piezas.get(pieza, '')
                
                # Crear casilla
                casilla = tk.Label(self.area_tablero, text=simbolo, bg=color, font=('Arial', 36), width=3, height=1)
                casilla.grid(row=fila, column=col, padx=1, pady=1)
        
        # Numeros de fila
        for i in range(8):
            num = tk.Label(self.area_tablero, text=str(8-i), font=('Arial', 10, 'bold'), bg='#1e1e2f', fg='#e0b973', width=2)
            num.grid(row=i, column=8, padx=5)
        
        # Letras de columna
        for i in range(8):
            letra = tk.Label(self.area_tablero, text=chr(ord('a')+i), font=('Arial', 10, 'bold'), bg='#1e1e2f', fg='#e0b973')
            letra.grid(row=8, column=i, pady=5)
    
    def mostrar_error(self, errores):
        texto_error = "Cadena FEN invalida\n\n" + "\n".join(errores)
        messagebox.showerror("Error", texto_error)
        self.mensaje.config(text="FEN invalido", fg='#e74c3c')


# Programa principal
def main():
    root = tk.Tk()
    app = Ventana(root)
    root.mainloop()


if __name__ == "__main__":
    main()