#  Sistema de Control de Acceso para Estudiantes y Visitantes

Este proyecto es una **aplicación de escritorio robusta y fácil de usar**, desarrollada en **Python** con `Tkinter` y una base de datos `SQLite`. Está diseñada para gestionar de manera eficiente el ingreso y la salida de estudiantes y visitantes en cualquier institución, ofreciendo una interfaz intuitiva para la administración y el registro de accesos.

---

## Características Principales

- **Interfaz Gráfica Moderna**: Construida con `Tkinter` y `ttk.Notebook` para una experiencia de usuario fluida y organizada.
- **Gestión de Estudiantes**:
  - Registro sencillo de estudiantes por parte del administrador.
  - Generación automática de un **PIN único** para cada estudiante, facilitando su acceso.
  - Registro de entrada y salida mediante PIN.
- **Gestión de Visitantes**:
  - Registro de visitantes con un **tiempo límite de estadía** configurable.
- **Base de Datos Integrada**: Utiliza **SQLite** para un almacenamiento de datos persistente y local.
- **Historial de Accesos Completo**:
  - Consulta detallada del historial de ingresos y salidas.
  - Exportación del historial a formato **CSV** para análisis o informes.
- **Validación de Datos Básica**: Asegura la integridad de la información ingresada.
- **Arquitectura Modular**: Código bien organizado en módulos (`main`, `admin`, `student_visitor`, `utils`, `db_setup`) para facilitar el mantenimiento y futuras expansiones.

---

##  Estructura del Proyecto
```
sistema_acceso/
├── main.py # Menú principal de la aplicación
├── student_visitor.py # Lógica para el registro de estudiantes y visitantes
├── admin.py # Módulo de administración (registro de estudiantes, exportación)
├── db_setup.py # Script para la creación inicial de la base de datos
├── utils.py # Funciones auxiliares y de utilidad
├── data/
│ └── acceso.db # Base de datos SQLite
└── README.md # Este archivo
```
---

## ⚙️ Requisitos

- **Python 3.7** o superior.
- ¡No se requieren librerías externas! Viene con todo lo que necesitas.

---

##  Cómo Empezar

Sigue estos sencillos pasos para poner en marcha el sistema:

1.  **Clona el repositorio** o descarga los archivos `ZIP` directamente.

2.  **Configura la base de datos** (¡solo una vez!):

    ```bash
    python db_setup.py
    ```

3.  **Ejecuta la aplicación**:
    ```bash
    python main.py
    ```

---

##  Acceso de Administrador

- **Usuario**: `—` (deja este campo vacío al iniciar sesión)
- **Contraseña**: `admin123` (¡Puedes cambiarla directamente en el archivo `admin.py` para mayor seguridad!)

---

##  Próximas Mejoras (Ideas Futuras)

- Implementar **alertas en tiempo real** si un visitante excede su tiempo límite.
- Mejorar la **seguridad del login** del administrador.
- Expandir las opciones de **exportación para incluir también los registros de visitantes**.
- Considerar una **migración a una aplicación web** utilizando frameworks como Flask o Django para un acceso más amplio.
- Crear un **instalador `.exe`** con PyInstaller para una distribución más fácil.

---

##  Licencia

Este proyecto está bajo la **Licencia MIT**. Eres libre de usarlo, modificarlo y distribuirlo, solo asegúrate de mantener la atribución original.

---

##  Autor

Desarrollado con pasión por *EM_DEV*. ¡Siéntete libre de personalizar y adaptar este proyecto a tus necesidades!
