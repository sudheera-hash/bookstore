from app import app, db
from models import User, Book
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    # Create admin user
    if not User.query.filter_by(email='admin@bookstore.com').first():
        admin = User(
            username='admin',
            email='admin@bookstore.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        print('Admin user created.')

    # Sample books
    books = [
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'genre': 'Fiction',
            'price': 9.99,
            'stock': 20,
            'description': 'A story of wealth, love, and the American Dream in the 1920s.',
            'cover_url': 'https://covers.openlibrary.org/b/id/8432895-L.jpg'
        },
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'genre': 'Fiction',
            'price': 11.99,
            'stock': 15,
            'description': 'A powerful story of racial injustice and loss of innocence in the American South.',
            'cover_url': 'https://covers.openlibrary.org/b/id/8810494-L.jpg'
        },
        {
            'title': 'A Brief History of Time',
            'author': 'Stephen Hawking',
            'genre': 'Science',
            'price': 14.99,
            'stock': 10,
            'description': 'An exploration of cosmology, black holes, and the nature of time.',
            'cover_url': 'https://covers.openlibrary.org/b/id/8353241-L.jpg'
        },
        {
            'title': 'Clean Code',
            'author': 'Robert C. Martin',
            'genre': 'Technology',
            'price': 29.99,
            'stock': 8,
            'description': 'A handbook of agile software craftsmanship for writing clean, maintainable code.',
            'cover_url': 'https://covers.openlibrary.org/b/id/8091016-L.jpg'
        },
        {
            'title': 'Sapiens',
            'author': 'Yuval Noah Harari',
            'genre': 'History',
            'price': 16.99,
            'stock': 25,
            'description': 'A brief history of humankind from the Stone Age to the present.',
            'cover_url': 'https://covers.openlibrary.org/b/id/8739161-L.jpg'
        },
        {
            'title': 'Atomic Habits',
            'author': 'James Clear',
            'genre': 'Self-Help',
            'price': 13.99,
            'stock': 30,
            'description': 'A proven framework for building good habits and breaking bad ones.',
            'cover_url': 'https://covers.openlibrary.org/b/id/10395911-L.jpg'
        },
    ]

    for b in books:
        if not Book.query.filter_by(title=b['title']).first():
            book = Book(**b)
            db.session.add(book)
            print(f"Added: {b['title']}")

    db.session.commit()
    print('Done!')