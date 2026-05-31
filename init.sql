CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    description TEXT,
    cover_url TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_price REAL NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

CREATE TABLE wishlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

INSERT INTO users (username, email, password_hash, is_admin) 
VALUES ('admin', 'admin@bookstore.com', 'scrypt:32768:8:1$M4Ryi5nBaY01Oits$e0a8624f122ba66569b598df0f237d828dc9a428f0a5cfd3e269aad9a77389c8c55578bd4b32e362cc69fc26cd85651f8ee02dc8ad3d647464ee44d185feab88', 1);

INSERT INTO books (title, author, genre, price, stock, description, cover_url) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 9.99, 20, 'A story of wealth, love, and the American Dream in the 1920s.', 'https://covers.openlibrary.org/b/id/8432895-L.jpg'),
('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 11.99, 15, 'A powerful story of racial injustice and loss of innocence in the American South.', 'https://covers.openlibrary.org/b/id/8810494-L.jpg'),
('A Brief History of Time', 'Stephen Hawking', 'Science', 14.99, 10, 'An exploration of cosmology, black holes, and the nature of time.', 'https://covers.openlibrary.org/b/id/8353241-L.jpg'),
('Clean Code', 'Robert C. Martin', 'Technology', 29.99, 8, 'A handbook of agile software craftsmanship for writing clean, maintainable code.', 'https://covers.openlibrary.org/b/id/8091016-L.jpg'),
('Sapiens', 'Yuval Noah Harari', 'History', 16.99, 25, 'A brief history of humankind from the Stone Age to the present.', 'https://covers.openlibrary.org/b/id/8739161-L.jpg'),
('Atomic Habits', 'James Clear', 'Self-Help', 13.99, 30, 'A proven framework for building good habits and breaking bad ones.', 'https://covers.openlibrary.org/b/id/10395911-L.jpg');