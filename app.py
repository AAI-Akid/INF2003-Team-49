from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key for sessions

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

    # Check if cart exists in session; if not, create it
    if 'cart' not in session:
        session['cart'] = []  # Initialize an empty cart if it doesn't exist

    # Append the book to the cart
    session['cart'].append(book)

    # Save the updated cart back to the session
    session.modified = True  # Mark session as modified to ensure changes are saved

    # Redirect to the dashboard
    return redirect(url_for('dashboard'))

@app.route('/cart')
def view_cart():
    # Get the cart from the session
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)  # Clear the cart from the session
    flash('Your cart has been cleared.')  # Optional: flash a message
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
            session.pop('cart', None)  # Clear the cart upon login
            return redirect(url_for('dashboard'))  # Redirect to dashboard

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

    return render_template('dashboard.html', user=user, books=books)


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user_id from the session
    return redirect(url_for('index'))  # Redirect to home page

# User Profile route
@app.route('/profile', methods=['GET', 'POST'])
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

    return render_template('profile.html', user=user)

# Ensure this block is at the end
if __name__ == '__main__':
    app.run(debug=True)
