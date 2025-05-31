import sqlite3


def init_db():
    conn = sqlite3.connect("acceso.db")
    cursor = conn.cursor()

    # Tabla de estudiantes: dni y pin únicos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            dni TEXT NOT NULL UNIQUE,
            telefono TEXT NOT NULL,
            curso TEXT NOT NULL,
            salon TEXT NOT NULL,
            pin TEXT NOT NULL UNIQUE
        )
    """)

    # Índices para mejorar velocidad de consultas por dni y pin
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_dni ON estudiantes(dni)")
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_pin ON estudiantes(pin)")

    # Tabla de registros de acceso con CHECK en activo para solo 0 o 1
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            rol TEXT NOT NULL,
            hora_entrada TEXT NOT NULL,
            hora_salida TEXT,
            activo INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0,1)),
            FOREIGN KEY(estudiante_id) REFERENCES estudiantes(id)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
