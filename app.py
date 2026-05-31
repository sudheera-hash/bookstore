from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['DATABASE'] = 'bookstore.db'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Helper to get database connection
def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# User class for flask-login
class User(UserMixin):
    def __init__(self, id, username, email, is_admin):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    db.close()
    if user:
        return User(user['id'], user['username'], user['email'], user['is_admin'])
    return None

# ---------- Home ----------
@app.route('/')
def index():
    genre = request.args.get('genre')
    search = request.args.get('search')
    db = get_db()
    
    query = 'SELECT * FROM books WHERE 1=1'
    params = []
    if genre:
        query += ' AND genre = ?'
        params.append(genre)
    if search:
        query += ' AND title LIKE ?'
        params.append(f'%{search}%')
    
    books = db.execute(query, params).fetchall()
    genres = db.execute('SELECT DISTINCT genre FROM books WHERE genre IS NOT NULL').fetchall()
    db.close()
    
    return render_template('index.html', books=books, genres=[g['genre'] for g in genres])

# ---------- Book detail ----------
@app.route('/book/<int:id>')
def book(id):
    db = get_db()
    book = db.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()
    db.close()
    if not book:
        return 'Book not found', 404
    return render_template('book.html', book=book)

# ---------- Cart ----------
@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    db = get_db()
    items = []
    total = 0
    for book_id, qty in cart.items():
        book = db.execute('SELECT * FROM books WHERE id = ?', (int(book_id),)).fetchone()
        if book:
            subtotal = book['price'] * qty
            total += subtotal
            items.append({'book': book, 'qty': qty, 'subtotal': subtotal})
    db.close()
    return render_template('cart.html', items=items, total=total)

@app.route('/cart/add/<int:book_id>', methods=['POST'])
@login_required
def add_to_cart(book_id):
    cart = session.get('cart', {})
    key = str(book_id)
    cart[key] = cart.get(key, 0) + 1
    session['cart'] = cart
    flash('Book added to cart!')
    return redirect(url_for('index'))

@app.route('/cart/remove/<int:book_id>', methods=['POST'])
@login_required
def remove_from_cart(book_id):
    cart = session.get('cart', {})
    cart.pop(str(book_id), None)
    session['cart'] = cart
    return redirect(url_for('cart'))

# ---------- Checkout ----------
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty.')
        return redirect(url_for('cart'))
    
    db = get_db()
    
    if request.method == 'POST':
        total = 0
        order_items = []
        for book_id, qty in cart.items():
            book = db.execute('SELECT * FROM books WHERE id = ?', (int(book_id),)).fetchone()
            if book and book['stock'] >= qty:
                total += book['price'] * qty
                order_items.append((book, qty))
        
        if not order_items:
            flash('Some items are out of stock.')
            db.close()
            return redirect(url_for('cart'))
        
        # Insert order
        cursor = db.execute(
            'INSERT INTO orders (user_id, total_price, status) VALUES (?, ?, ?)',
            (current_user.id, total, 'pending')
        )
        order_id = cursor.lastrowid
        
        # Insert order items and update stock
        for book, qty in order_items:
            db.execute(
                'INSERT INTO order_items (order_id, book_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
                (order_id, book['id'], qty, book['price'])
            )
            db.execute('UPDATE books SET stock = stock - ? WHERE id = ?', (qty, book['id']))
        
        db.commit()
        db.close()
        session['cart'] = {}
        flash('Order placed successfully!')
        return redirect(url_for('orders'))
    
    items = []
    total = 0
    for book_id, qty in cart.items():
        book = db.execute('SELECT * FROM books WHERE id = ?', (int(book_id),)).fetchone()
        if book:
            subtotal = book['price'] * qty
            total += subtotal
            items.append({'book': book, 'qty': qty, 'subtotal': subtotal})
    db.close()
    return render_template('checkout.html', items=items, total=total)

# ---------- Orders ----------
@app.route('/orders')
@login_required
def orders():
    db = get_db()
    user_orders = db.execute(
        'SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC',
        (current_user.id,)
    ).fetchall()
    
    # Get items for each order
    orders_with_items = []
    for order in user_orders:
        items = db.execute(
            'SELECT oi.*, b.title, b.author FROM order_items oi JOIN books b ON oi.book_id = b.id WHERE oi.order_id = ?',
            (order['id'],)
        ).fetchall()
        orders_with_items.append({'order': order, 'items': items})
    
    db.close()
    return render_template('orders.html', orders=orders_with_items)

# ---------- Wishlist ----------
@app.route('/wishlist')
@login_required
def wishlist():
    db = get_db()
    items = db.execute(
        'SELECT w.*, b.* FROM wishlist w JOIN books b ON w.book_id = b.id WHERE w.user_id = ?',
        (current_user.id,)
    ).fetchall()
    db.close()
    return render_template('wishlist.html', items=items)

@app.route('/wishlist/add/<int:book_id>', methods=['POST'])
@login_required
def add_to_wishlist(book_id):
    db = get_db()
    existing = db.execute(
        'SELECT * FROM wishlist WHERE user_id = ? AND book_id = ?',
        (current_user.id, book_id)
    ).fetchone()
    if not existing:
        db.execute(
            'INSERT INTO wishlist (user_id, book_id) VALUES (?, ?)',
            (current_user.id, book_id)
        )
        db.commit()
        flash('Added to wishlist!')
    else:
        flash('Already in your wishlist.')
    db.close()
    return redirect(url_for('book', id=book_id))

@app.route('/wishlist/remove/<int:book_id>', methods=['POST'])
@login_required
def remove_from_wishlist(book_id):
    db = get_db()
    db.execute(
        'DELETE FROM wishlist WHERE user_id = ? AND book_id = ?',
        (current_user.id, book_id)
    )
    db.commit()
    db.close()
    flash('Removed from wishlist.')
    return redirect(url_for('wishlist'))

# ---------- Auth ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        existing = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            flash('Email already registered.')
            db.close()
            return redirect(url_for('register'))
        
        db.execute(
            'INSERT INTO users (username, email, password_hash, is_admin) VALUES (?, ?, ?, ?)',
            (username, email, generate_password_hash(password), 0)
        )
        db.commit()
        db.close()
        flash('Account created! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        db.close()
        
        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['id'], user['username'], user['email'], user['is_admin'])
            login_user(user_obj)
            return redirect(url_for('index'))
        flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('cart', None)
    return redirect(url_for('index'))

# ---------- Admin ----------
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    db = get_db()
    books = db.execute('SELECT * FROM books').fetchall()
    orders = db.execute('SELECT * FROM orders ORDER BY created_at DESC').fetchall()
    total_revenue = db.execute('SELECT SUM(total_price) as total FROM orders').fetchone()['total'] or 0
    db.close()
    return render_template('admin/dashboard.html', books=books, orders=orders, total_revenue=total_revenue)

@app.route('/admin/book/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_book():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            'INSERT INTO books (title, author, genre, price, stock, description, cover_url) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (
                request.form['title'],
                request.form['author'],
                request.form['genre'],
                float(request.form['price']),
                int(request.form['stock']),
                request.form['description'],
                request.form['cover_url']
            )
        )
        db.commit()
        db.close()
        flash('Book added successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/add_book.html')

@app.route('/admin/book/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_book(id):
    db = get_db()
    db.execute('DELETE FROM books WHERE id = ?', (id,))
    db.commit()
    db.close()
    flash('Book deleted.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/order/<int:order_id>/status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    db = get_db()
    db.execute('UPDATE orders SET status = ? WHERE id = ?', (request.form['status'], order_id))
    db.commit()
    db.close()
    flash('Order status updated.')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)