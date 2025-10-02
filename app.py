from flask import Flask # importando a classe Flask da biblioteca flask

app = Flask(__name__)

# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/')
def hello_world():
    return 'Hello, World!'
    # print('Hello, World!')

if __name__ == '__main__':
    app.run(debug = True)