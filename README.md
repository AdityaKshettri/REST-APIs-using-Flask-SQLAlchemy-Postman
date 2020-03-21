# REST-APIs-using-Flask-SQLAlchemy-Postman
In this project, I have worked with Flask to create REST APIs for all CRUD operations for Book Management through SQLAlchemy and Postman using Python 3.8

# How to run this project:

1- Download the project, unzip it, go to the folder and the folder in command prompt.

2- To run the app without any database involved, just run the app_standalone.py file
> python app_standalone.py

3- To run the app with database, run the app.py file
> python app.py

4- In both the above cases, a server will be opened on port 5000

5- Open POSTMAN and login to get the security token.
> localhost:5000/login

6- Play with various REST API request using the token to get the json response.
> localhost:5000/books
