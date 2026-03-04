from flask import Flask, render_template, request, redirect, url_for
from logic.gestor_notas import GestorNotas
from models.documento import Documento

app = Flask(__name__)

gestor = GestorNotas()

gestor.obtener_datos_db()

# --- 3. RUTAS DE FLASK (Controladores) ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/nota/<int:id_nota>')
def ver_nota_individual(id_nota: int):
    nota_encontrada = gestor.documentos.get(id_nota)
    if nota_encontrada is None:
        return "Error 404: La nota que buscas no existe en la bóveda", 404
    return render_template("nota_individual.html", nota=nota_encontrada)

@app.route('/notas')
def ver_notas():
    mis_notas_reales = list(gestor.documentos.values())
    return render_template('notas.html', lista_notas=mis_notas_reales)

@app.route('/crear_nota', methods=['GET', 'POST'])
def crear_nota():
    # Si la petición es POST, significa que el usuario presionó el botón "Guardar" en el formulario
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        contenido_raw = request.form.get('contenido_raw')

        try:
            # Instanciamos el documento. El ID y la fecha se generan automáticamente en la base de datos
            nuevo_doc = Documento(id_documento=None, titulo=titulo, contenido_raw=contenido_raw, fecha_creacion=None)
            gestor.agregar_documento(nuevo_doc)
            # Si todo sale bien, lo redirigimos a la lista principal de notas
            return redirect(url_for('ver_notas'))
        except ValueError as e:
            return f"Error de validación: {e}", 400

    # Si la petición es GET, solo le mostramos la página con el formulario vacío
    return render_template('crear_nota.html')

@app.route('/editar_nota/<int:id_nota>', methods=['GET', 'POST'])
def editar_nota(id_nota: int):
    nota = gestor.documentos.get(id_nota)
    if not nota:
        return "Error 404: La nota no existe", 404

    if request.method == 'POST':
        nuevo_texto = request.form.get('contenido_raw')
        try:
            gestor.actualizar_contenido(id_nota, nuevo_texto)
            return redirect(url_for('ver_nota_individual', id_nota=id_nota))
        except Exception as e:
            return f"Error al actualizar la base de datos: {e}", 500

    # Si es GET, le mandamos la nota al template para que los campos ya vengan llenos
    return render_template('editar_nota.html', nota=nota)

@app.route('/eliminar_nota/<int:id_nota>', methods=['POST'])
def eliminar_nota(id_nota: int):
    try:
        gestor.eliminar_documento(id_nota)
        return redirect(url_for('ver_notas'))
    except Exception as e:
        return f"Error al eliminar de la base de datos: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)