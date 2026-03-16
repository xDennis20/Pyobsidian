from http.cookiejar import cut_port_re

from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_manager import DatabaseManager
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from logic.gestor_notas import GestorNotas
from models.documento import Documento
from models.usuario import Usuario

app = Flask(__name__)
app.secret_key = '13456'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a tu bóveda.'

# --- RUTAS DE FLASK (Controladores) ---
@app.route('/')
@login_required
def home():
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    conexion = None
    try:
        conexion = DatabaseManager().obtener_conexion()
        cursor = conexion.cursor()
        query = "SELECT id, username, es_admin FROM public.usuario WHERE id = %s"
        cursor.execute(query, (int(user_id),))
        user_record = cursor.fetchone()
        cursor.close()

        if user_record:
            return Usuario(id=user_record[0], username=user_record[1], es_admin=user_record[2])
        return None
    except Exception as e:
        print(f"Error cargando usuario: {e}")
        return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    # ... (Tu código de registro está perfecto, lo dejamos igual) ...
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Por favor, completa todos los campos.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        conexion = None
        try:
            conexion = DatabaseManager().obtener_conexion()
            cursor = conexion.cursor()
            query = """
                    INSERT INTO public.usuario (username, password_hash)
                    VALUES (%s, %s)
                    """
            cursor.execute(query, (username, hashed_password))
            conexion.commit()
            cursor.close()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect(url_for('login'))
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error en BD: {e}")
            flash('Error: El nombre de usuario ya está en uso o hubo un problema.')
            return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Por favor, ingresa tu usuario y contraseña.')
            return redirect(url_for('login'))

        conexion = None
        try:
            conexion = DatabaseManager().obtener_conexion()
            cursor = conexion.cursor()
            query = "SELECT id, username, password_hash, es_admin FROM public.usuario WHERE username = %s"
            cursor.execute(query, (username,))
            user_record = cursor.fetchone()
            cursor.close()

            if user_record and check_password_hash(user_record[2], password):
                usuario_obj = Usuario(id=user_record[0], username=user_record[1], es_admin=user_record[3])
                login_user(usuario_obj)
                flash('¡Bienvenido de nuevo a tu bóveda!')
                return redirect(url_for('ver_notas'))
            else:
                flash('Usuario o contraseña incorrectos.')
                return redirect(url_for('login'))
        except Exception as e:
            print(f"Error en BD al iniciar sesión: {e}")
            flash('Hubo un problema interno al intentar iniciar sesión.')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente. ¡Nos vemos!')
    return redirect(url_for('login'))


@app.route('/mis-notas-privadas')
@login_required
def notas_privadas():
    return "Bienvenido a tus apuntes secretos de PyObsidian."


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/notas')
@login_required
def ver_notas():
    gestor = GestorNotas()
    gestor.obtener_datos_db(current_user.id)
    mis_notas_reales = list(gestor.documentos.values())
    return render_template('notas.html', lista_notas=mis_notas_reales)

@app.route('/nota/<int:id_nota>')
@login_required
def ver_nota_individual(id_nota: int):
    gestor = GestorNotas()
    gestor.obtener_datos_db(current_user.id)
    nota_encontrada = gestor.documentos.get(id_nota)

    if nota_encontrada is None:
        return "Error 404: La nota que buscas no existe en tu bóveda o no te pertenece", 404
    return render_template("nota_individual.html", nota=nota_encontrada)

@app.route('/crear_nota', methods=['GET', 'POST'])
@login_required
def crear_nota():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        contenido_raw = request.form.get('contenido_raw')

        gestor = GestorNotas()
        try:
            nuevo_doc = Documento(id_documento=None, titulo=titulo, contenido_raw=contenido_raw, fecha_creacion=None,usuario_id=current_user.id)
            gestor.agregar_documento(nuevo_doc)
            return redirect(url_for('ver_notas'))
        except ValueError as e:
            return f"Error de validación: {e}", 400

    return render_template('crear_nota.html')

@app.route('/editar_nota/<int:id_nota>', methods=['GET', 'POST'])
@login_required
def editar_nota(id_nota: int):
    gestor = GestorNotas()
    gestor.obtener_datos_db(current_user.id)
    nota = gestor.documentos.get(id_nota)

    if not nota:
        return "Error 404: La nota no existe o no tienes permisos", 404

    if request.method == 'POST':
        nuevo_texto = request.form.get('contenido_raw')
        try:
            gestor.actualizar_contenido(id_nota, nuevo_texto, current_user.id)
            return redirect(url_for('ver_nota_individual', id_nota=id_nota))
        except Exception as e:
            return f"Error al actualizar la base de datos: {e}", 500

    return render_template('editar_nota.html', nota=nota)


@app.route('/eliminar_nota/<int:id_nota>', methods=['POST'])
@login_required
def eliminar_nota(id_nota: int):
    gestor = GestorNotas()
    gestor.obtener_datos_db(current_user.id)
    nota = gestor.documentos.get(id_nota)

    if not nota:
        return "Error: No tienes permiso para borrar esto", 403

    try:
        gestor.eliminar_documento(id_nota, current_user.id)
        return redirect(url_for('ver_notas'))
    except Exception as e:
        return f"Error al eliminar de la base de datos: {e}", 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)