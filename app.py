from flask import Flask, request, jsonify # importando as classes Flask, request e jsonify da biblioteca flask
from flask_sqlalchemy import SQLAlchemy # importando a classe SQLAlchemy da biblioteca flask_sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db' # acessar o atributo chamado config e dar o nome do nosso banco de ecommerce.db

db = SQLAlchemy(app) # criando a variável db e conectando no meu app via SQLAlchemy passando como parâmetro meu app flask

# Modelagem
# Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False) # esse campo pode ter até 120 caracteres e não pode ser nulo
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.Text, nullable = True) # esse campo não tem limitação no tamanho do texto e é opcional

@app.route('/api/products/add', methods = ['POST']) # Rota para adicionar um produto
def add_product():
    data = request.json
    if 'name' in data and 'price' in data: # verifica se a chave 'name' e 'price' existe dentro de data e então inicia cadastro
        # product = Product(name = data['name'], price = ['price'], description = ['description'])
        product = Product(name = data.get('name'), price = data.get('price'), description = data.get('description', ''))
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully!'}), 200
    return jsonify({'message': 'Invalid product data'}), 400

@app.route('/api/products/delete/<int:product_id>', methods = ['DELETE']) # rota para deletar um produto a partir do product_id
def delete_product(product_id):
    product = Product.query.get(product_id) # Recupera o produto da nossa base de dados
    if product: # Verifica se o produto existe, ou seja, se ele é válido
        db.session.delete(product) # Se existir, deleta da base de dados
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully!'}), 200
    return jsonify({'message': 'Product not found'}), 404 # Se não existir, retorna 404 not found

# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/')
def hello_world():
    return 'Hello, World!'
    # print('Hello, World!')

if __name__ == '__main__':
    app.run(debug = True)