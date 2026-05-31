# 📚 BookStore — E-Commerce Web Application

A full-stack e-commerce bookstore built with **Flask, SQLite, and pure SQL**. Users can browse books, add to cart/wishlist, and checkout. Admins can manage inventory and view sales analytics.

## Features

### User Features
- ✅ Browse and search books by title or genre
- ✅ Add books to cart and wishlist
- ✅ User authentication (register/login)
- ✅ Checkout and place orders
- ✅ View order history

### Admin Features
- ✅ Add, edit, and delete books
- ✅ Manage inventory and stock levels
- ✅ View all orders and revenue dashboard
- ✅ Update order status (pending/shipped)

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite with raw SQL queries
- **Frontend:** HTML, CSS
- **Authentication:** Flask-Login

## Installation

### Prerequisites
- Python 3.7+
- pip

### Setup

1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/bookstore.git
cd bookstore
```

2. Install dependencies
```bash
pip install flask flask-login werkzeug
```

3. Initialize the database
```bash
sqlite3 bookstore.db < init.sql
```

4. Run the application
```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

## Admin Login

- **Email:** `admin@bookstore.com`
- **Password:** `admin123`

## Project Structure
bookstore/
├── app.py                    # Main Flask app with all routes
├── bookstore.db             # SQLite database
├── init.sql                 # Database schema & sample data
├── templates/               # HTML templates
│   ├── base.html           # Base layout
│   ├── index.html          # Home/book listing
│   ├── book.html           # Book detail page
│   ├── cart.html           # Shopping cart
│   ├── checkout.html       # Checkout form
│   ├── orders.html         # Order history
│   ├── wishlist.html       # Wishlist
│   ├── login.html          # Login page
│   ├── register.html       # Register page
│   └── admin/
│       ├── dashboard.html  # Admin dashboard
│       └── add_book.html   # Add book form
└── static/
└── style.css           # Styling

## Database Schema

- **users** — User accounts (username, email, password, admin flag)
- **books** — Book inventory (title, author, genre, price, stock)
- **orders** — User orders with total price and status
- **order_items** — Individual items in each order
- **wishlist** — User wishlists

## Portfolio Features

This project demonstrates:
- **Raw SQL queries** — No ORM, pure SQL for learning
- **CRUD operations** — Create, Read, Update, Delete books and orders
- **Authentication** — User login/register with hashed passwords
- **Session management** — Shopping cart using Flask sessions
- **Database design** — Proper foreign keys and relationships
- **Full-stack development** — Backend, database, frontend

## Future Enhancements

- [ ] Payment gateway integration
- [ ] Book reviews and ratings
- [ ] Search filters and pagination
- [ ] Email notifications
- [ ] Admin user management
- [ ] Book categories/subcategories

## Author

Sudheera uthpala - [GitHub](https://github.com/YOUR_USERNAME)

## License

MIT License