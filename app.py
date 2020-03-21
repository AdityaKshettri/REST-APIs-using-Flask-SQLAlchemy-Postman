from flask import Flask, jsonify, request, Response
import json
import jwt
import datetime
from functools import wraps

from BookModel import Book
from UserModel import User
from settings import *


app.config['SECRET_KEY'] = 'meow'

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid token to view this page'}), 401
    return wrapper

@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])
    match = User.username_password_match(username, password)
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm = 'HS256')
        return token
    else:
        return Response("", 401, mimetype='application/json')

#Home
@app.route('/')
def hello_world():
    return 'Hello World!'

#GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})

#GET /books/<isbn>
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)

#validating POST Request Data
def validPostRequestData(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False
    
#POST /books
@app.route('/books', methods=['POST'])
@token_required
def add_book():
    request_data = request.get_json()
    if(validPostRequestData(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", status = 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidPostRequestDataErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 10, 'id': 4}"
        }
        response = Response(json.dumps(invalidPostRequestDataErrorMsg), status=400, mimetype='application/json')
        return response

#validating PUT Request Data
def validPutRequestData(bookObject):
    if ("name" in bookObject and "price" in bookObject):
        return True
    else:
        return False

#PUT /books/<isbn>
@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
    request_data = request.get_json()
    if(validPutRequestData(request_data)):
        Book.replace_book(isbn, request_data['name'], request_data['price']) 
        response = Response("", status = 204)
        return response
    else:
        invalidPutRequestDataErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 10}"
        }
        response = Response(json.dumps(invalidPutRequestDataErrorMsg), status=400, mimetype='application/json')
        return response

#PATCH /books/<isbn>
@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()
    if("name" in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if("price" in request_data):
        Book.update_book_name(isbn, request_data['price'])
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

#DELETE /books/<isbn>
@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        response = Response("", status=204)
        return response
    invalidIdErrorMsg = {
        "error": "Invalid book isbn passed in request"
    }
    response = Response(json.dumps(invalidIdErrorMsg), status = 404, mimetype = 'application/json')
    return response;

app.run(port=5000)
