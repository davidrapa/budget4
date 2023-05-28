import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True

data = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    total = {}
    if request.method == 'POST':
        action = request.form['action']
        for key in request.form:
            data[key] = request.form.get(key)
        if action == 'Resta':
            total = calculate_total()
            plot_graph(total)
    return render_template('index.html', data=data, total=total)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


def calculate_total():
    total = {}
    for i in range(1, 13):
        ingresos = float(data.get(f'ingresos_{i}', '0') or '0')
        gastos = float(data.get(f'gastos_{i}', '0') or '0')
        gastos_tarjeta_de_credito = float(data.get(f'gastos_tarjeta_de_credito_{i}', '0') or '0')
        gastos_auto = float(data.get(f'gastos_auto_{i}', '0') or '0')
        gastos_alquiler = float(data.get(f'gastos_alquiler_{i}', '0') or '0')

        total[i] = ingresos - gastos - gastos_tarjeta_de_credito - gastos_auto - gastos_alquiler

    return total


def plot_graph(total):
    months = np.arange(1, 13)
    ingresos = [float(data.get(f'ingresos_{i}', '0') or '0') for i in range(1, 13)]
    gastos = [float(data.get(f'gastos_{i}', '0') or '0') for i in range(1, 13)]

    plt.figure()
    plt.plot(months, ingresos, label='Ingresos')
    plt.plot(months, gastos, label='Egresos')
    plt.xlabel('Meses')
    plt.ylabel('Cantidad')
    plt.title('Ingresos y Egresos por Mes')
    plt.legend()
    plt.savefig('static/graph.png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
