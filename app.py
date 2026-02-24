from flask import Flask,render_template
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/notas')
def ver_notas():
    mis_notas = [
        {"titulo": "Aprendiendo Flask", "tag": "#dev"},
        {"titulo": "Rutina de Calistenia", "tag": "#salud"},
        {"titulo": "Configuración de Fedora", "tag": "#linux"}
    ]
    return render_template('notas.html', lista_notas=mis_notas)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
