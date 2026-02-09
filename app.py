from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():  # put application's code here
    return "<h1> Bienvenidos a Pyobsidian <h1><p>Tu sistema de notas en Markdown.</p>"

@app.route("/nota/<titulo>")
def ver_nota(titulo: str):
    return f"""
    <h2>Viendo la nota: {titulo} <h2>
    <p>Aquí se mostraría el contenido procesado de Markdown a HTML para la nota "{titulo}".</p>
    <br>
    <a href="/">Volver al inicio</a>
    """
if __name__ == '__main__':
    app.run(debug=True)
