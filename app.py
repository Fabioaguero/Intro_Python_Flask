# imports
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

#Modelagem DB
#Produtos (id, name, price, description, color e no futuro image)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(30), nullable=True)

#Criação de Rotas API's
#Api de cadastramento de produto via método POST
@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""), color=data.get("color", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"mensage": "Produto cadastrado com sucesso!"})
    return jsonify({"mensage": "Invalid product data"}), 400

#API de deleção de produto via método DELEtE
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
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

# @app.route('/api/login')
# @app.route('/api/logout')
# @app.route('/api/products')
# @app.route('/api/products/')
# @app.route('/api/products/search')
# @app.route('/api/products/uptade')
# @app.route('/api/card/add')
# @app.route('/api/card/remove')
# @app.route('/api/card')
# @app.route('/api/card/chekout')


# Definir uma rota raiz (pagina inicial) e a funcao que sera executada ao requisitar 
@app.route('/')
def hellow_word():
    return 'Hellow Word'

if __name__ == "__main__":
    app.run(debug=True)