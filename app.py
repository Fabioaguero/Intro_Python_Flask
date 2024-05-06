# imports
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha_chave_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

#Modelagem DB
#Usuario ADMIN
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    
    

#Produtos (id, name, price, description, color e no futuro image)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(30), nullable=True)

#Autenticação de uduarios
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    

#Criação de Rotas API's
#API de autenticação
@app.route('/login', methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(username=data.get("username")).first()

    if user and data.get("password") == user.password :
            login_user(user)
            return jsonify({"message": "Logged in successfully"})
        
    return jsonify({"message": "Unauthorized. Invalid credentials"}), 401

@app.route('/logout', methods=["POST"])

#API de produtos e buscas

#API de listagem de produtos no banco de dados
@app.route('/api/products', methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
              "id": product.id,
              "name": product.name,
              "price": product.price,
              "description": product.description,
              "color": product.color           
        }
        product_list.append(product_data)

    return jsonify(product_list)

@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
              "id": product.id,
              "name": product.name,
              "price": product.price,
              "description": product.description,
              "color": product.color
        })
    return jsonify({"message": "Produto not found"}), 404

# @app.route('/api/products/search')

#API de CRUD 
#Api de cadastramento de produto via método POST
@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""), color=data.get("color", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"mensage": "Produto cadastrado com sucesso!"})
    return jsonify({"mensage": "Invalid product data"}), 400

#API de deleção de produto via método DELETE
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    #Recuperação do produto da base de dados
    product = Product.query.get(product_id)
    #Verificar se o produto exite (é valido) 
    if product:
       #se existe, apagar o produto do banco de dados
        db.session.delete(product)
        db.session.commit()
        return jsonify({"mensage": "Produto deletado com sucesso!"})
    return jsonify({"mensage": "Product not found"}), 404

#API de atualização de produto via método UPDATE
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"mensage": "Product not found"}), 404
    
    data = request.json 
    if 'name'in data:
        product.name = data['name'] 

    if 'price'in data:
        product.price = data['price'] 

    if 'description'in data:
        product.description = data['description'] 

    if 'color'in data:
        product.color = data['color'] 
        
    db.session.commit()    

    return jsonify({"mensage": "Produto alterado com sucesso!"})    

# @app.route('/api/card/remove')


#API de carrinho de compra
# @app.route('/api/card/add')
# @app.route('/api/card')
# @app.route('/api/card/chekout')


# Definir uma rota raiz (pagina inicial) e a funcao que sera executada ao requisitar 
@app.route('/')
def hellow_word():
    return 'Hellow Word'

if __name__ == "__main__":
    app.run(debug=True)