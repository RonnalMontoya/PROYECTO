from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Inicio')

@app.route('/about/')
def about():
    return render_template('about.html', title='Acerca de')

@app.route('/contactos/')
def contactos():
    return render_template('contactos.html', title='Contactos')

if __name__ == '__main__':
    app.run(debug=True)
