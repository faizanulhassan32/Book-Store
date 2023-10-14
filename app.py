from flask import Flask, render_template, request, redirect, url_for , jsonify
from pymongo import MongoClient
import os


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/BookStore_Application'

client = MongoClient('mongodb://localhost:27017/')
db = client.get_database('BookStore_Application')
mycollection = db.get_collection('books')


@app.route('/')
def index():
    books = mycollection.find()
    return render_template('index.html' , books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == 'Admin@gmail.com' and password == 'Admin123':
            return redirect(url_for('afterlogin'))
        else:
            return render_template('index.html', message='Invalid email or password')
    else:
        return render_template('index.html')


@app.route('/afterlogin')
def afterlogin():
    books = mycollection.find()
    return render_template('afterlogin.html' , books=books)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/add_book', methods=['POST'])
def add_book():
    # Get the book information from the form
    name = request.form['name']
    picture = request.files['picture']
    pdf = request.files['pdf']

    # Save the uploaded files to a folder on your server
    picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture.filename).replace('\\', '/')
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename).replace('\\', '/')
    picture.save(picture_path)
    pdf.save(pdf_path)

    # Create a document with the book information
    document = {
        'name': name,
        'picture_path': picture_path,
        'pdf_path': pdf_path
    }

    # Insert the document into the "books" collection
    mycollection.insert_one(document)

    books = mycollection.find()
    return render_template('afterlogin.html' , books=books)    





if __name__ == '__main__':
    app.run(debug=True)