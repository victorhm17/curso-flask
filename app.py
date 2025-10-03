from flask import Flask, request, jsonify # importando as classes Flask, request e jsonify da biblioteca flask
from flask_sqlalchemy import SQLAlchemy # importando a classe SQLAlchemy da biblioteca flask_sqlalchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'XPTO_123' # chave para habilitar o LoginManager
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db' # acessar o atributo chamado config e dar o nome do nosso banco de ecommerce.db

login_manager = LoginManager()
db = SQLAlchemy(app) # criando a variável db e conectando no meu app via SQLAlchemy passando como parâmetro meu app flask
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app) # agora conseguimos acessar o swagger de qualquer lugar

# modelagem das tabelas User e Product
# usuario (id, username, password)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False, unique = True) # esse campo pode ter até 30 caracteres, não pode ser nulo e deve ser único
    password = db.Column(db.String(80), nullable = False)
'''
flask shell
user = User(username="admin", password="123")
db.session.add(user)
db.sessions.commit())
exit()
'''

# produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False) # esse campo pode ter até 120 caracteres e não pode ser nulo
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.Text, nullable = True) # esse campo não tem limitação no tamanho do texto e é opcional

# autenticação
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods = ['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username = data.get('username')).first() # Recupera o primeiro username da nossa base de dados
    
    if user and data.get('password') == user.password:
        login_user(user)
        return jsonify({'message': 'Logged in successfully'})
    return jsonify({'messagem': 'Unauthorized. Invalid credentials'}), 401

@app.route('/logout', methods = ['POST'])
@login_required # eu preciso estar logado para então conseguir fazer o logout
def logout():
    logout_user()
    return jsonify({'message': 'Logout successfully'})

# rota para adicionar um produto
@app.route('/api/products/add', methods = ['POST'])
@login_required # eu preciso estar logado para acessar a rota acima
def add_product():
    data = request.json
    if 'name' in data and 'price' in data: # verifica se a chave 'name' e 'price' existe dentro de data e então inicia cadastro
        product = Product(name = data.get('name'), price = data.get('price'), description = data.get('description', ''))
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully!'}), 200
    return jsonify({'message': 'Invalid product data'}), 400

# rota para recuperar toda lista de produtos
@app.route('/api/products', methods = ['GET'])
def get_products():
    products = Product.query.all()
    products_list = []

    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'price': product.price
        }
        products_list.append(product_data)
    return jsonify(products_list)

# rota para recuperar detalhes de um produto a partir do product_id
@app.route('/api/products/<int:product_id>', methods = ['GET'])
def get_product_details(product_id):
    product = Product.query.get(product_id) # Recupera o produto da nossa base de dados
    if product: # Verifica se o produto existe, ou seja, se ele é válido
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description
        })
    return jsonify({'message': 'Product not found'}), 404 # Se não existir, retorna 404 not found

# rota para atualizar detalhes de um produto a partir do product_id
@app.route('/api/products/update/<int:product_id>', methods = ['PUT'])
@login_required # eu preciso estar logado para acessar a rota acima
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404 # Se não encontrar um produto para atualizar, retorna not found

    data = request.json
    # verifica se as chaves 'name', 'price' e 'description' existem em 'data' e então atualiza cadastro com o que veio na request
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']

    db.session.commit()

    return jsonify({'message': 'Product updated successfully!'})

# rota para deletar um produto a partir do product_id
@app.route('/api/products/delete/<int:product_id>', methods = ['DELETE'])
@login_required # eu preciso estar logado para acessar a rota acima
def delete_product(product_id):
    product = Product.query.get(product_id) # Recupera o produto da nossa base de dados
    if product: # Verifica se o produto existe, ou seja, se ele é válido
        db.session.delete(product) # Se existir, deleta da base de dados
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully!'}), 200
    return jsonify({'message': 'Product not found'}), 404 # Se não existir, retorna 404 not found

# definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/')
def hello_world():
    return 'Hello, World!'
    # print('Hello, World!')

if __name__ == '__main__':
    app.run(debug = True)