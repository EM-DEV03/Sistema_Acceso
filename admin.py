import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import sqlite3
from datetime import datetime
import csv


class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Módulo Administrador")
        self.root.geometry("900x600")

        if not self.login():
            self.root.destroy()
            return

        self.build_interface()
        self.load_students()
        self.load_records()

    def login(self):
        password = simpledialog.askstring(
            "Login Admin", "Ingrese la contraseña de administrador:", show="*"
        )
        if password == "admin123":
            return True
        else:
            messagebox.showerror("Error", "Contraseña incorrecta. Acceso denegado.")
            return False

    def build_interface(self):
        self.tabControl = ttk.Notebook(self.root)
        self.tab_students = ttk.Frame(self.tabControl)
        self.tab_records = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_students, text="Gestión de Estudiantes")
        self.tabControl.add(self.tab_records, text="Registros de Acceso")
        self.tabControl.pack(expand=1, fill="both")

        # --- TAB ESTUDIANTES ---
        frm = ttk.Frame(self.tab_students, padding=10)
        frm.pack(fill="both", expand=True)

        cols = ("id", "nombre", "dni", "telefono", "curso", "salon", "pin")
        self.tree_students = ttk.Treeview(frm, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree_students.heading(c, text=c.capitalize())
            self.tree_students.column(c, width=100, anchor="center")
        self.tree_students.pack(side="left", fill="both", expand=True)
        self.tree_students.bind("<<TreeviewSelect>>", self.on_student_select)

        scrollbar = ttk.Scrollbar(
            frm, orient="vertical", command=self.tree_students.yview
        )
        self.tree_students.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="left", fill="y")

        btn_frame = ttk.Frame(self.tab_students)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Agregar Estudiante", command=self.add_student).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(btn_frame, text="Editar Estudiante", command=self.edit_student).grid(
            row=0, column=1, padx=5
        )
        ttk.Button(
            btn_frame, text="Eliminar Estudiante", command=self.delete_student
        ).grid(row=0, column=2, padx=5)

        # --- TAB REGISTROS ---
        frm2 = ttk.Frame(self.tab_records, padding=10)
        frm2.pack(fill="both", expand=True)

        cols_r = ("id", "nombre", "rol", "hora_entrada", "hora_salida", "activo")
        self.tree_records = ttk.Treeview(
            frm2, columns=cols_r, show="headings", height=20
        )
        for c in cols_r:
            self.tree_records.heading(c, text=c.capitalize())
            self.tree_records.column(c, width=120, anchor="center")
        self.tree_records.pack(side="left", fill="both", expand=True)

        scrollbar_r = ttk.Scrollbar(
            frm2, orient="vertical", command=self.tree_records.yview
        )
        self.tree_records.configure(yscroll=scrollbar_r.set)
        scrollbar_r.pack(side="left", fill="y")

        btn_frame_r = ttk.Frame(self.tab_records)
        btn_frame_r.pack(pady=10)

        ttk.Button(
            btn_frame_r, text="Actualizar Registros", command=self.load_records
        ).grid(row=0, column=0, padx=5)
        ttk.Button(
            btn_frame_r,
            text="Usuarios Actualmente en Campus",
            command=self.show_active_users,
        ).grid(row=0, column=1, padx=5)
        ttk.Button(
            btn_frame_r, text="Exportar Registros a CSV", command=self.export_csv
        ).grid(row=0, column=2, padx=5)

    def run_query(self, query, parameters=()):
        with sqlite3.connect("acceso.db") as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def load_students(self):
        for row in self.tree_students.get_children():
            self.tree_students.delete(row)
        query = "SELECT id, nombre, dni, telefono, curso, salon, pin FROM estudiantes"
        rows = self.run_query(query)
        for r in rows:
            self.tree_students.insert("", "end", values=r)

    def load_records(self):
        for row in self.tree_records.get_children():
            self.tree_records.delete(row)
        query = "SELECT id, nombre, rol, hora_entrada, hora_salida, activo FROM registros ORDER BY hora_entrada DESC"
        rows = self.run_query(query)
        for r in rows:
            activo_text = "Dentro" if r[5] == 1 else "Fuera"
            self.tree_records.insert(
                "",
                "end",
                values=(r[0], r[1], r[2], r[3], r[4] if r[4] else "-", activo_text),
            )

    def add_student(self):
        StudentForm(self, "Agregar Estudiante")

    def edit_student(self):
        selected = self.tree_students.selection()
        if not selected:
            messagebox.showwarning(
                "Advertencia", "Seleccione un estudiante para editar."
            )
            return
        data = self.tree_students.item(selected[0], "values")
        StudentForm(self, "Editar Estudiante", data)

    def delete_student(self):
        selected = self.tree_students.selection()
        if not selected:
            messagebox.showwarning(
                "Advertencia", "Seleccione un estudiante para eliminar."
            )
            return
        data = self.tree_students.item(selected[0], "values")
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar estudiante {data[1]}?")
        if confirm:
            self.run_query("DELETE FROM estudiantes WHERE id = ?", (data[0],))
            self.load_students()
            messagebox.showinfo("Eliminado", "Estudiante eliminado correctamente.")

    def on_student_select(self, event):
        pass  # Aquí podrías mostrar detalles o habilitar botones según selección

    def show_active_users(self):
        rows = self.run_query("SELECT nombre, rol FROM registros WHERE activo = 1")
        if rows:
            users = "\n".join([f"{r[0]} ({r[1]})" for r in rows])
            messagebox.showinfo(
                "Usuarios Activos",
                f"Usuarios actualmente dentro del campus:\n\n{users}",
            )
        else:
            messagebox.showinfo(
                "Usuarios Activos", "No hay usuarios actualmente dentro del campus."
            )

    def export_csv(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
        )
        if not file:
            return
        rows = self.run_query(
            "SELECT id, nombre, rol, hora_entrada, hora_salida, activo FROM registros ORDER BY hora_entrada DESC"
        )
        with open(file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["ID", "Nombre", "Rol", "Hora Entrada", "Hora Salida", "Estado"]
            )
            for r in rows:
                estado = "Dentro" if r[5] == 1 else "Fuera"
                writer.writerow([r[0], r[1], r[2], r[3], r[4] if r[4] else "-", estado])
        messagebox.showinfo("Exportar CSV", "Registros exportados exitosamente.")


class StudentForm(tk.Toplevel):
    def __init__(self, parent, title, data=None):
        super().__init__(parent.root)
        self.parent = parent
        self.title(title)
        self.geometry("400x400")
        self.resizable(False, False)
        self.data = data
        self.build_form()
        if data:
            self.load_data()

    def build_form(self):
        frm = ttk.Frame(self, padding=20)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Nombre Completo:").grid(row=0, column=0, sticky="w")
        self.entry_nombre = ttk.Entry(frm, width=40)
        self.entry_nombre.grid(row=0, column=1, pady=5)

        ttk.Label(frm, text="DNI:").grid(row=1, column=0, sticky="w")
        self.entry_dni = ttk.Entry(frm, width=40)
        self.entry_dni.grid(row=1, column=1, pady=5)

        ttk.Label(frm, text="Teléfono:").grid(row=2, column=0, sticky="w")
        self.entry_telefono = ttk.Entry(frm, width=40)
        self.entry_telefono.grid(row=2, column=1, pady=5)

        ttk.Label(frm, text="Curso:").grid(row=3, column=0, sticky="w")
        self.entry_curso = ttk.Entry(frm, width=40)
        self.entry_curso.grid(row=3, column=1, pady=5)

        ttk.Label(frm, text="Salón:").grid(row=4, column=0, sticky="w")
        self.entry_salon = ttk.Entry(frm, width=40)
        self.entry_salon.grid(row=4, column=1, pady=5)

        ttk.Label(frm, text="PIN (Se genera automáticamente al agregar)").grid(
            row=5, column=0, columnspan=2, pady=10
        )

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

        ttk.Button(btn_frame, text="Guardar", command=self.save_student).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).grid(
            row=0, column=1, padx=5
        )

    def load_data(self):
        self.entry_nombre.insert(0, self.data[1])
        self.entry_dni.insert(0, self.data[2])
        self.entry_telefono.insert(0, self.data[3])
        self.entry_curso.insert(0, self.data[4])
        self.entry_salon.insert(0, self.data[5])

    def generate_pin(self):
        import random

        return str(random.randint(1000, 9999))

    def save_student(self):
        nombre = self.entry_nombre.get().strip()
        dni = self.entry_dni.get().strip()
        telefono = self.entry_telefono.get().strip()
        curso = self.entry_curso.get().strip()
        salon = self.entry_salon.get().strip()

        if not (nombre and dni and telefono and curso and salon):
            messagebox.showwarning("Validación", "Todos los campos son obligatorios.")
            return

        if self.data:
            # Editar estudiante
            query = """UPDATE estudiantes SET nombre=?, dni=?, telefono=?, curso=?, salon=? WHERE id=?"""
            self.parent.run_query(
                query, (nombre, dni, telefono, curso, salon, self.data[0])
            )
            messagebox.showinfo("Éxito", "Estudiante actualizado correctamente.")
        else:
            # Agregar estudiante con PIN único
            pin = self.generate_pin()
            # Verificar si pin ya existe
            existing = self.parent.run_query(
                "SELECT * FROM estudiantes WHERE pin = ?", (pin,)
            ).fetchone()
            while existing:
                pin = self.generate_pin()
                existing = self.parent.run_query(
                    "SELECT * FROM estudiantes WHERE pin = ?", (pin,)
                ).fetchone()
            query = """INSERT INTO estudiantes (nombre, dni, telefono, curso, salon, pin) VALUES (?, ?, ?, ?, ?, ?)"""
            self.parent.run_query(query, (nombre, dni, telefono, curso, salon, pin))
            messagebox.showinfo(
                "Éxito", f"Estudiante agregado correctamente.\nPIN asignado: {pin}"
            )

        self.parent.load_students()
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminApp(root)
    root.mainloop()
