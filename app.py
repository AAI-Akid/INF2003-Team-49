import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from decimal import Decimal
import mysql.connector
import bcrypt


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key for session
app.config['STATIC_FOLDER'] = 'static'


# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Your MySQL username
        password='NiSSanr34!',  # Your MySQL password
        database='bookstore',
        port=3306  # default is 3306
    )

# Home page to display books
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM books')  # Fetch all books
    books = cursor.fetchall()  # Get the results as a list of dictionaries
    conn.close()

    user = None  # Replace with your user session logic to get the logged-in user, if any

    return render_template('index.html', books=books, user=user)  # Pass books and user to the template


# ** ADMIN FUNCTIONALITY **

# Admin page to manage books
@app.route('/admin')
def admin():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_page'))  # Redirect if not admin

    books = get_all_books()  # Fetch all books from the database
    return render_template('admin.html', books=books)

# Function to fetch all books from the database
def get_all_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM books')  # Adjust based on your database schema
    books = cursor.fetchall()
    conn.close()
    return books

# Allowed file types
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = 'static/images/books'  # Ensure this directory exists

# Allowed file types
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}  
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/admin/add_book', methods=['POST'])
def add_book():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_page'))  # Redirect if not admin

    title = request.form['title']
    author = request.form['author']
    price = request.form['price']

    if not title or not author or not price:
        flash('All fields are required!')
        return redirect(url_for('admin'))

    # Handle file upload
    if 'cover_image' not in request.files:
        flash('No file part')
        return redirect(url_for('admin'))

    file = request.files['cover_image']  # Ensure this matches your HTML input name
    
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('admin'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Connect to the database
        conn = get_db_connection()  # Make sure you have this function defined
        cursor = conn.cursor()

        # Insert book details into the database, including the cover_image filename
        cursor.execute(
            'INSERT INTO books (title, author, price, cover_image) VALUES (%s, %s, %s, %s)',
            (title, author, price, filename)
        )
        conn.commit()
        conn.close()

        flash('Book added successfully!')
        return redirect(url_for('admin'))

    else:
        flash('Invalid file type! Only JPG, JPEG, and PNG are allowed.')
        return redirect(url_for('admin'))


# Fetch book by ID
def get_book_by_id(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM books WHERE book_id = %s', (book_id,))
    book = cursor.fetchone()
    conn.close()
    return book

# Update book details
def update_book(book_id, title, author, rating, price, currency, description, publisher, page_count, genres, isbn, language, published_date, cover_image_filename):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE books 
        SET title = %s, author = %s, rating = %s, price = %s, currency = %s, description = %s, 
        publisher = %s, page_count = %s, generes = %s, isbn = %s, language = %s, 
        published_date = %s, cover_image = %s 
        WHERE book_id = %s
        ''',
        (title, author, rating, price, currency, description, publisher, page_count, genres, isbn, language, published_date, cover_image_filename, book_id)
    )
    conn.commit()
    conn.close()


@app.route('/admin/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_page'))  # Redirect if not admin

    # Fetch the current book data to populate the form (GET request)
    book = get_book_by_id(book_id)

    if request.method == 'GET':
        return render_template('edit_book.html', book=book)

    # Handle form submission (POST request)
    if request.method == 'POST':
        # Fetch the submitted form data
        title = request.form.get('title') or book['title']
        author = request.form.get('author') or book['author']
        rating = request.form.get('rating') or book['rating']
        price = request.form.get('price') or book['price']
        currency = request.form.get('currency') or book['currency']
        description = request.form.get('description') or book['description']
        publisher = request.form.get('publisher') or book['publisher']
        page_count = request.form.get('page_count') or book['page_count']
        genres = request.form.get('genres') or book['genres']
        isbn = request.form.get('isbn') or book['isbn']
        language = request.form.get('language') or book['language']
        published_date = request.form.get('published_date') or book['published_date']

        # Handle file upload if an image is submitted
        cover_image = request.files.get('cover_image')
        if cover_image:
            cover_image_filename = secure_filename(cover_image.filename)
            cover_image.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_image_filename))
        else:
            cover_image_filename = book['cover_image']  # Use existing image if no new one is uploaded

        # Update the book with the new or unchanged values
        update_book(book_id, title, author, rating, price, currency, description, publisher, page_count, genres, isbn, language, published_date, cover_image_filename)

        flash('Book updated successfully!')
        return redirect(url_for('admin'))


# Admin route to delete a book
@app.route('/admin/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_page'))  # Redirect if not admin

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE book_id = %s', (book_id,))
    conn.commit()
    conn.close()

    flash('Book deleted successfully!')
    return redirect(url_for('admin'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/orders')
def admin_view_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT o.order_id, o.user_id, o.order_date, o.status, o.total_price, oi.quantity, oi.price_per_unit, b.title, u.email
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN books b ON oi.book_id = b.book_id
        JOIN users u ON o.user_id = u.user_id
        ORDER BY o.order_date DESC
    """)

    orders_data = cursor.fetchall()
    orders = {}
    for row in orders_data:
        order_id = row['order_id']
        if order_id not in orders:
            orders[order_id] = {
                'order_id': order_id,
                'user_id': row['user_id'],
                'email': row['email'],
                'order_date': row['order_date'],
                'status': row['status'],
                'total_price': row['total_price'],
                'items': []  # Initialize as an empty list
            }
        orders[order_id]['items'].append({
            'title': row['title'],
            'quantity': row['quantity'],
            'price_per_unit': row['price_per_unit']
        })
    print(f"OADASDASDASD: {orders.values()}")  # Print the orders for debugging
    cursor.close()
    conn.close()

    # Convert orders dictionary to a list for template rendering
    return render_template('view_orders.html', orders=orders.values())


# ** CART FUNCTIONALITY **

@app.route('/add_to_cart/<int:book_id>', methods=['POST'])  # Allow POST requests
def add_to_cart(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Insert the book into the cart_items table
        cursor.execute("SELECT book_id, title, price, currency FROM books WHERE book_id = %s", (book_id,))
        book = cursor.fetchone()
        if book:
            # Initialize the cart if it doesn't exist in the session
            if 'cart' not in session:
                session['cart'] = []

            # Check if the book is already in the cart
            cart = session['cart']
            for item in cart:
                if item['book_id'] == book_id:
                    item['quantity'] += 1
                    break
            else:
                # Add the book to cart
                cart.append({'book_id': book_id, 
                             'title': book[1],
                             'price': book[2], 
                             'currency': book[3], 
                             'quantity': 1})

            session['cart'] = cart  # Update the cart in the session
            flash(f'{book[1]} added to cart successfully.')
        else:
            flash('Book not found.')

    except mysql.connector.Error as err:
        print(f"Error: {err}")  # Print the error for debugging
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('dashboard'))  # Redirect back to dashboard after adding to cart



@app.route('/cart')
def view_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    cart = session.get('cart', [])  # Retrieve the cart from the session
    total_price = sum(Decimal(item['price']) * item['quantity'] for item in cart)

    return render_template('cart.html', cart_items=cart, total_price=total_price)


@app.route('/clear_cart')
def clear_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    # Clear the cart from the session
    session.pop('cart', None)
    flash('Your cart has been cleared.')

    return redirect(url_for('view_cart'))  # Redirect to the cart page




# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Insert a new user (user_id is auto-incremented)
            cursor.execute('INSERT INTO users (username, email, password, address) VALUES (%s, %s, %s, %s)',
                           (username, email, hashed_password, address))
            conn.commit()
            flash('Sign up successful! Please log in.')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}')
        finally:
            conn.close()

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('Please enter both email and password.')
            return render_template('login.html')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = user['user_id']  # Store user ID in session
            session['role'] = user['role']  # Store user role in session (e.g., 'user' or 'admin')
            session.pop('cart', None)  # Clear the cart upon login
            
            if user['role'] == 'admin':
                return redirect(url_for('admin'))  # Redirect to admin page if user is admin
            else:
                return redirect(url_for('dashboard'))  # Redirect to user dashboard

        else:
            flash('Invalid email or password!')

    return render_template('login.html')



# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    conn = get_db_connection()
    
    # Fetch the current user
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (session['user_id'],))
    user = cursor.fetchone()

    # Fetch the books
    cursor.execute('SELECT * FROM books')  # Adjust this query if your books table is named differently
    books = cursor.fetchall()  # Fetch all books

    conn.close()

    return render_template('dashboard.html', users=user, books=books)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = get_book_by_id(book_id)
    
    if book is None:
        flash('Book not found.')  # Notify the user if the book does not exist
        return redirect(url_for('dashboard'))  # Redirect to the dashboard or another appropriate page
    
    return render_template('book_detail.html', book=book)


def get_book_by_id(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch the book by its ID
    cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    # Check if the book was found
    if book is not None:
        return book  # Return the entire book dictionary
    else:
        return None  # Return None if no book was found

    
    if book:
        # Convert the result to a dictionary or appropriate format
        return {
            'book_id': book[0],
            'title': book[1],
            'author': book[2],
            'rating': book[3],
            'price': book[4],
            'currency': book[5],
            'description': book[6],
            'publisher': book[7],
            'page_count': book[8],
            'generes': book[9],
            'ISBN': book[10],
            'language': book[11],
            'published_date': book[12],
            'cover_image': book[13]  # Assuming you have a cover image URL in the database
        }
    else:
        return None  # Handle the case where no book is found

@app.route('/logout')
def logout():
    session.clear()  # Clear the user session
    return redirect(url_for('index'))  # Redirect to index page after logout


# User Profile route
@app.route('/user_profile', methods=['GET', 'POST'])
def profile():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        new_email = request.form['email']
        new_password = request.form['password']  # Ensure this is hashed as well
        new_address = request.form['address']

        # Update user info in the database
        cursor.execute('UPDATE users SET email = %s, password = %s, address = %s WHERE user_id = %s',
                       (new_email, bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()), new_address, session['user_id']))
        conn.commit()
        flash('Profile updated successfully')
        return redirect(url_for('profile'))

    cursor.execute('SELECT * FROM users WHERE user_id = %s', (session['user_id'],))
    user = cursor.fetchone()
    conn.close()

    return render_template('user_profile.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    conn = get_db_connection()  # Establish a new connection
    cursor = conn.cursor(dictionary=True)

    # Retrieve user info from the database
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (session['user_id'],))
    user = cursor.fetchone()

    if request.method == 'POST':
        new_email = request.form['email']
        new_address = request.form['address']
        new_password = request.form['password']

        # Prepare the query and parameters for the update
        if new_password:  # Only hash and include the new password if it's provided
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('UPDATE users SET email = %s, password = %s, address = %s WHERE user_id = %s',
                           (new_email, hashed_password, new_address, session['user_id']))
        else:
            cursor.execute('UPDATE users SET email = %s, address = %s WHERE user_id = %s',
                           (new_email, new_address, session['user_id']))

        conn.commit()
        flash('Profile updated successfully')
        return redirect(url_for('profile'))

    conn.close()  # Close the database connection
    return render_template('edit_profile.html', user=user)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch cart items for the user
    cart = session.get('cart', [])  # Retrieve the cart from the session (list of dictionaries)
    total_price = sum(Decimal(item['price']) * item['quantity'] for item in cart)

    if request.method == 'POST' and cart:
        # Insert new order into the orders table
        cursor.execute('INSERT INTO orders (user_id, order_date, status, total_price) VALUES (%s, NOW(), %s, %s)',
                       (session['user_id'], 'Pending', total_price))
        conn.commit()
        order_id = cursor.lastrowid  # Get the ID of the last inserted order

        # Insert each item in the cart into the order_items table
        for item in cart:
            cursor.execute('INSERT INTO order_items (order_id, book_id, quantity, price_per_unit) VALUES (%s, %s, %s, %s)',
                           (order_id, item['book_id'], item['quantity'], item['price']))
            conn.commit()

        # Clear the cart after successful checkout
        session.pop('cart', None)
        flash('Checkout successful! Your order has been placed.')
        return redirect(url_for('index'))  # Redirect after successful checkout

    return render_template('checkout.html', cart_items=cart, total_price=total_price)
    

@app.route('/remove_item', methods=['POST'])
def remove_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Ensure the user is logged in

    item_id = request.form['item_id']  # Get the item_id from the form

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete the item from the cart using cart_items.id
        cursor.execute('DELETE FROM cart_items WHERE user_id = %s AND id = %s', (session['user_id'], item_id))  # Use item_id
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")  # Log any error for debugging
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('view_cart'))  # Redirect back to the cart view


if __name__ == '__main__':
    app.run(debug=True)


