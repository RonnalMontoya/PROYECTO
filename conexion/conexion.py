# conexion/conexion.py
import mysql.connector

# Función para abrir conexión
def conexion():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          # Usuario por defecto en XAMPP
            password="",          # Si tu root no tiene clave, déjalo vacío
            database="proyecto"   # Nombre de tu base en phpMyAdmin
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Función para cerrar conexión
def cerrar_conexion(conn):
    if conn and conn.is_connected():
        conn.close()
