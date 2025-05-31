import tkinter as tk
from tkinter import ttk
from student_visitor import StudentVisitorApp
from admin import AdminApp


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Acceso Principal")
        self.root.geometry("320x220")
        self.build_interface()

    def build_interface(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Seleccione una opción", font=("Arial", 14)).pack(pady=10)

        ttk.Button(
            frame,
            text="Estudiante / Visitante",
            width=30,
            command=self.open_student_visitor,
        ).pack(pady=10)

        ttk.Button(frame, text="Administrador", width=30, command=self.open_admin).pack(
            pady=10
        )

    def open_student_visitor(self):
        new_window = tk.Toplevel(self.root)
        StudentVisitorApp(new_window)

    def open_admin(self):
        new_window = tk.Toplevel(self.root)
        AdminApp(new_window)


if __name__ == "__main__":
    root = tk.Tk()
    MainApp(root)
    root.mainloop()