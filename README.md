# 🥖 Sistema de Inventario - Panadería EL PANCITO CRIOLLO

Este proyecto es un **sistema de gestión de inventarios** desarrollado en **Python con Flask**, que permite administrar los productos de una panadería.  
El sistema implementa persistencia múltiple utilizando:

- 📄 **Archivos locales**: TXT, JSON, CSV  
- 🗄 **Base de datos relacional**: MySQL  
- 🌐 **Interfaz web**: Flask + Bootstrap  

---

## 🚀 Funcionalidades

✅ Añadir productos con nombre, cantidad y precio  
✅ Listar productos en una tabla interactiva  
✅ Editar y eliminar productos  
✅ Guardar datos en TXT, JSON, CSV y MySQL simultáneamente  
✅ Consultar datos desde distintas fuentes  
✅ Interfaz moderna con **Bootstrap 5**  
✅ Sistema de **login y registro de usuarios** con **Flask-Login + MySQL**  

---

## 📂 Script de la Base de Datos

El proyecto incluye el archivo **`database/proyecto.sql`**, que contiene la estructura y datos iniciales de la base de datos MySQL.

🔧 Cómo importar la base de datos

- Abre tu terminal y entra a MySQL:
   ```bash
   mysql -u root -p
- Crea la base de datos:
CREATE DATABASE proyecto;
USE proyecto;

- Importa el script:
source database/proyecto.sql;
✅ Esto creará las tablas y cargará los datos.

🚀 Ejecución del Proyecto
- Instalar dependencias:
pip install -r requirements.txt
- Ejecutar Flask:
python app.py
- Abrir en el navegador:
http://127.0.0.1:5000

👨‍💻 Tecnologías utilizadas
•	Python 3
•	Flask
•	Flask-Login
•	MySQL
•	SQLAlchemy
•	Bootstrap 5

📌 Autor: Ronnal Montoya
📅 Año: 2025



