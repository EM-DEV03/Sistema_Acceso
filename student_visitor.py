import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


class StudentVisitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ingreso Estudiante/Visitante")
        self.root.geometry("400x300")
        self.build_interface()

    def build_interface(self):
        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.pack(expand=True, fill="both")

        ttk.Label(self.frame, text="Ingreso de Estudiantes", font=("Arial", 14)).pack(
            pady=10
        )

        ttk.Label(self.frame, text="Ingrese su PIN:").pack()
        self.pin_entry = ttk.Entry(self.frame, show="*")
        self.pin_entry.pack(pady=5)

        ttk.Button(
            self.frame, text="Registrar Entrada/Salida", command=self.handle_pin
        ).pack(pady=10)

    def handle_pin(self):
        pin = self.pin_entry.get()
        if not pin:
            messagebox.showwarning("Advertencia", "Debe ingresar el PIN")
            return

        conn = sqlite3.connect("acceso.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM estudiantes WHERE pin = ?", (pin,))
        estudiante = cursor.fetchone()

        if not estudiante:
            messagebox.showerror("Error", "PIN no encontrado")
            conn.close()
            return

        estudiante_id = estudiante[0]
        nombre = estudiante[1]
        rol = "Estudiante"
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "SELECT * FROM registros WHERE estudiante_id = ? AND activo = 1",
            (estudiante_id,),
        )
        registro_activo = cursor.fetchone()

        if registro_activo:
            # Registrar salida
            cursor.execute(
                "UPDATE registros SET hora_salida = ?, activo = 0 WHERE id = ?",
                (ahora, registro_activo[0]),
            )
            conn.commit()
            messagebox.showinfo("Salida registrada", f"{nombre} ha salido del campus.")
        else:
            # Registrar entrada
            cursor.execute(
                """
                INSERT INTO registros (estudiante_id, nombre, rol, hora_entrada, activo)
                VALUES (?, ?, ?, ?, 1)
            """,
                (estudiante_id, nombre, rol, ahora),
            )
            conn.commit()
            messagebox.showinfo(
                "Entrada registrada", f"{nombre} ha ingresado al campus."
            )

        conn.close()
        self.pin_entry.delete(0, tk.END)
