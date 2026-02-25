from flask import Flask, render_template
from logic.gestor_notas import GestorNotas

app = Flask(__name__)

print("--- Iniciando todos las acciones de las notas de PyObsidian ---")
gestor = GestorNotas()

print("Conectando a PostgreSQL para cargar notas...")
gestor.obtener_datos_db()
print(f"¡Carga completada! {len(gestor.documentos)} notas en memoria listas para usarse.")


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
    return render_template("nota_individual.html",nota=nota_encontrada)
@app.route('/notas')
def ver_notas():
    mis_notas_reales = list(gestor.documentos.values())
    return render_template('notas.html', lista_notas=mis_notas_reales)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
