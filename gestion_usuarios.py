import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "usuarios.db"

def crear_base_datos():
    """Crea la base de datos y la tabla de usuarios si no existe"""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()


def hash_password(password):
    """Genera un hash SHA-256 de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()


def agregar_usuario(nombre, password):
    """Agrega un usuario nuevo con su contraseña en hash"""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    password_hasheada = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)",
            (nombre, password_hasheada)
        )
        conexion.commit()
        print(f"Usuario '{nombre}' agregado correctamente.")
    except sqlite3.IntegrityError:
        print(f"El usuario '{nombre}' ya existe.")
    conexion.close()


def validar_usuario(nombre, password):
    """Valida si el usuario y contraseña coinciden con lo almacenado"""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (nombre,))
    resultado = cursor.fetchone()
    conexion.close()

    if resultado is None:
        return False

    password_hasheada = hash_password(password)
    return resultado[0] == password_hasheada


@app.route("/")
def inicio():
    return "<h1>Sitio de Gestión de Usuarios - Examen DRY7122</h1>"


@app.route("/validar", methods=["POST"])
def validar():
    """Endpoint para validar usuario vía POST con JSON: {"nombre": "...", "password": "..."}"""
    datos = request.get_json()
    nombre = datos.get("nombre")
    password = datos.get("password")

    if validar_usuario(nombre, password):
        return jsonify({"resultado": "Usuario válido"}), 200
    else:
        return jsonify({"resultado": "Usuario o contraseña incorrectos"}), 401


if __name__ == "__main__":
    crear_base_datos()

    # Cargar usuarios del examen (integrantes del grupo)
    agregar_usuario("Javier Garrido", "clave123")

    print("\n--- Validando usuario de prueba ---")
    print(validar_usuario("Javier Garrido", "clave123"))  # True
    print(validar_usuario("Javier Garrido", "clave_mala"))  # False

    print("\nIniciando servidor en puerto 7500...")
    app.run(host="0.0.0.0", port=7500, debug=True)
