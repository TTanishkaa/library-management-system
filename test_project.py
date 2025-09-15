# test_project.py

from project import add_book, search_books, issue_book, connect_db, create_tables, register_user, login, return_book

def test_add_book():
    create_tables()  # Ensure tables exist
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title = 'Test Book'")
    conn.commit()
    conn.close()

    add_book("Test Book", "Test Author", 2023)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, year FROM books WHERE title = 'Test Book'")
    book = cursor.fetchone()
    conn.close()

    assert book == ("Test Book", "Test Author", 2023)

def test_search_books():
    create_tables()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title = 'Search Test'")
    cursor.execute("INSERT INTO books (title, author, year) VALUES ('Search Test', 'Author', 2020)")
    conn.commit()
    conn.close()

    books = search_books("Search")
    assert len(books) >= 1
    assert any("Search Test" in book for book in books)

def test_issue_book():
    create_tables()
    # Register a test user
    register_user("testuser", "testpass")
    user = login("testuser", "testpass")
    user_id = user[0]

    # Add a test book
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title = 'Issue Test'")
    cursor.execute("INSERT INTO books (title, author, year) VALUES ('Issue Test', 'Author', 2021)")
    book_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    success = issue_book(user_id, book_id)
    assert success

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM books WHERE book_id = ?", (book_id,))
    status = cursor.fetchone()[0]
    conn.close()

    assert status == 'issued'

    # Clean up
    return_book(book_id)
