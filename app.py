from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Your MySQL username
        password='P3n15w@nk3r',  # Your MySQL password
        database='bookstore',
        port=3307
    )

# Home page to display books
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

# Admin page to add new books
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, author, price) VALUES (%s, %s, %s)',
                       (title, author, price))
        conn.commit()
        conn.close()

        return redirect(url_for('admin'))

    return render_template('admin.html')

# Cart functionality
cart = []

@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
    book = cursor.fetchone()
    conn.close()

    cart.append(book)
    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
    return render_template('cart.html', cart=cart)

if __name__ == '__main__':
    app.run(debug=True)
