from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
# Set up our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init Marshmallow
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
    # Define our fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    # Create the constructor
    def __init__(self, name, description, price, qty) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

# Init our schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# We are going to init our db through the console
# on the python terminal brings in the db variable and call the create_all() method 
# from app import db
# db.create_all() : to create our db.sqlite

# Create our routes
# Create a Product
@app.route('/product', methods=['POST'])
def create_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product), 201

# Fetch all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result), 200

# Fetch Single product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product), 200

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty
    
    db.session.commit()

    return product_schema.jsonify(product), 201

# Delete Single product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id) # We need this line to know which product to delete
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product), 200 # Return the deleted object


# Create a basic route
# @app.route('/', methods=['GET'])
# def get():
#     return jsonify({ 'msg': 'Hello World' })

# Run Server
if __name__ == '__main__':
    app.run(debug=True)