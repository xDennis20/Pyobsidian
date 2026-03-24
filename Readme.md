# Pyobsidian 📝🕸️

Pyobsidian es una aplicación web inspirada en Obsidian, diseñada para funcionar como una base de conocimiento personal. Permite a los usuarios crear, gestionar y visualizar notas escritas en Markdown, renderizándolas dinámicamente en HTML.

## 🚀 Características Principales

* **Renderizado Dinámico:** Conversión en tiempo real de texto Markdown a etiquetas HTML limpias.
* **Gestión de Usuarios:** Sistema de autenticación seguro (Login/Logout) protegido con `flask-login`.
* **Persistencia de Datos:** Conexión robusta a base de datos PostgreSQL mediante `psycopg2`.
* **Arquitectura Modular:** Código estructurado separando la lógica de negocio, modelos de datos y conexión a la base de datos para facilitar la escalabilidad.

## 🛠️ Tecnologías y Herramientas (Tech Stack)

* **Backend:** Python 3, Flask
* **Base de Datos:** PostgreSQL (`psycopg2-binary`)
* **Procesamiento de Texto:** `Markdown`
* **Autenticación:** `Flask-Login`, `itsdangerous`
* **Frontend:** HTML5, CSS3, Jinja2 (Motor de plantillas)
* **Servidor de Producción:** `gunicorn`

## 📁 Estructura del Proyecto

El proyecto sigue una arquitectura limpia basada en la separación de responsabilidades:

```text
Pyobsidian/
├── database/         # Gestión de la conexión y consultas SQL (db_manager.py)
├── logic/            # Reglas de negocio (convertidor.py, gestor_notas.py)
├── models/           # Clases que representan las entidades (usuario.py, documento.py)
├── static/           # Archivos estáticos (styles.css)
├── templates/        # Vistas HTML renderizadas por Jinja2
├── app.py            # Punto de entrada principal de la aplicación Flask
└── requirements.txt  # Dependencias del proyecto 
```
# Instalación y Configuración Local
Sigue estos pasos para ejecutar el proyecto en tu máquina local:

**Clonar el repositorio:**

```text
git clone [https://github.com/TU_USUARIO/pyobsidian.git](https://github.com/TU_USUARIO/pyobsidian.git)
cd pyobsidian
```

**Crear y activar el entorno virtual:**
```text 
python -m venv .venv 
```
**En Windows:**
```text
.venv\Scripts\activate
```
**En Linux/Mac:**
```text
source .venv/bin/activate
```

**Instalar las dependencias:**

```bash
pip install -r requirements.txt
```

**Configurar la Base de Datos:**

Asegúrate de tener PostgreSQL instalado y en ejecución.

Crea una base de datos para el proyecto.

(Nota: Configura tus credenciales de conexión en el archivo correspondiente o mediante variables de entorno).

Ejecutar la aplicación (Modo Desarrollo):

```text
flask run
```

La aplicación estará disponible en http://127.0.0.1:5000