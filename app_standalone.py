from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)

books = [
    {
        'name': 'Harry Potter',
        'price': 100,
        'isbn': 1
    },
    {
        'name': 'David Copperfield',
        'price': 200,
        'isbn': 2
    }
]

#Home
@app.route('/')
def hello_world():
    return 'Hello World!'

#GET /books
@app.route('/books')
def get_books():
    return jsonify({'books':books})

#GET /books/<isbn>
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)

#validating POST Request Data
def validPostRequestData(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False
    
#POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validPostRequestData(request_data)):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
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
def replace_book(isbn):
    request_data = request.get_json()
    if(validPutRequestData(request_data)):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": isbn
        }
        i=0;
        for book in books:
            currentIsbn = book["isbn"]
            if(currentIsbn == isbn):
                books[i] = new_book
            i += 1
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
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if("name" in request_data):
        updated_book["name"] = request_data['name']
    if("price" in request_data):
        updated_book["price"] = request_data['price']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

#DELETE /books/<isbn>
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0;
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status = 204)
            return response
        i += 1
    invalidIdErrorMsg = {
        "error": "Invalid book id passed in request"
    }
    response = Response(json.dumps(invalidIdErrorMsg), status = 404, mimetype = 'application/json')
    return response;

app.run(port=5000)
