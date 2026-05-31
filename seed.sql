-- Insert admin user
INSERT INTO users (username, email, password_hash, is_admin) 
VALUES ('admin', 'admin@bookstore.com', 'pbkdf2:sha256:600000$xyzzz$abcdef123456', 1);

-- Insert sample books
INSERT INTO books (title, author, genre, price, stock, description, cover_url) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 9.99, 20, 'A story of wealth, love, and the American Dream in the 1920s.', 'https://covers.openlibrary.org/b/id/8432895-L.jpg'),
('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 11.99, 15, 'A powerful story of racial injustice and loss of innocence in the American South.', 'https://covers.openlibrary.org/b/id/8810494-L.jpg'),
('A Brief History of Time', 'Stephen Hawking', 'Science', 14.99, 10, 'An exploration of cosmology, black holes, and the nature of time.', 'https://covers.openlibrary.org/b/id/8353241-L.jpg'),
('Clean Code', 'Robert C. Martin', 'Technology', 29.99, 8, 'A handbook of agile software craftsmanship for writing clean, maintainable code.', 'https://covers.openlibrary.org/b/id/8091016-L.jpg'),
('Sapiens', 'Yuval Noah Harari', 'History', 16.99, 25, 'A brief history of humankind from the Stone Age to the present.', 'https://covers.openlibrary.org/b/id/8739161-L.jpg'),
('Atomic Habits', 'James Clear', 'Self-Help', 13.99, 30, 'A proven framework for building good habits and breaking bad ones.', 'https://covers.openlibrary.org/b/id/10395911-L.jpg');