import sqlite3
import sys

def connect_db():
    conn = sqlite3.connect('library.db')
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            status TEXT DEFAULT 'available'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issued_books (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_id INTEGER,
            issue_date DATE,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password, is_admin=0):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, password, is_admin))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, is_admin FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def add_book(title, author, year):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    conn.close()
    print(f"Book '{title}' added successfully.")

def search_books(keyword):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT book_id, title, author, year, status FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
    books = cursor.fetchall()
    conn.close()
    return books

def issue_book(user_id, book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM books WHERE book_id = ?", (book_id,))
    status = cursor.fetchone()
    if status and status[0] == 'available':
        cursor.execute("UPDATE books SET status = 'issued' WHERE book_id = ?", (book_id,))
        cursor.execute("INSERT INTO issued_books (user_id, book_id, issue_date) VALUES (?, ?, DATE('now'))", (user_id, book_id))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def return_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM books WHERE book_id = ?", (book_id,))
    status = cursor.fetchone()
    if status and status[0] == 'issued':
        cursor.execute("UPDATE books SET status = 'available' WHERE book_id = ?", (book_id,))
        cursor.execute("DELETE FROM issued_books WHERE book_id = ?", (book_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def list_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT book_id, title, author, year, status FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def view_issued_books(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.book_id, b.title, b.author, b.year, ib.issue_date
        FROM issued_books ib
        JOIN books b ON ib.book_id = b.book_id
        WHERE ib.user_id = ?
    """, (user_id,))
    issued = cursor.fetchall()
    conn.close()
    return issued

def admin_menu(user_id):
    while True:
        print("\nAdmin Menu:")
        print("1. Add Book")
        print("2. List All Books")
        print("3. Search Books")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Register New User")
        print("7. Logout")
        choice = input("Enter choice: ")
        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            year = int(input("Enter year: "))
            add_book(title, author, year)
        elif choice == '2':
            books = list_books()
            for book in books:
                print(book)
        elif choice == '3':
            keyword = input("Enter keyword: ")
            books = search_books(keyword)
            for book in books:
                print(book)
        elif choice == '4':
            book_id = int(input("Enter book ID: "))
            user = int(input("Enter user ID to issue to: "))
            if issue_book(user, book_id):
                print("Book issued successfully.")
            else:
                print("Book not available or doesn't exist.")
        elif choice == '5':
            book_id = int(input("Enter book ID: "))
            if return_book(book_id):
                print("Book returned successfully.")
            else:
                print("Book not issued or doesn't exist.")
        elif choice == '6':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if register_user(username, password):
                print("User registered successfully.")
            else:
                print("Username already exists.")
        elif choice == '7':
            break
        else:
            print("Invalid choice.")

def user_menu(user_id):
    while True:
        print("\nUser Menu:")
        print("1. List All Books")
        print("2. Search Books")
        print("3. View Issued Books")
        print("4. Logout")
        choice = input("Enter choice: ")
        if choice == '1':
            books = list_books()
            for book in books:
                print(book)
        elif choice == '2':
            keyword = input("Enter keyword: ")
            books = search_books(keyword)
            for book in books:
                print(book)
        elif choice == '3':
            issued = view_issued_books(user_id)
            for book in issued:
                print(book)
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

def main():
    create_tables()
    if not login("admin", "admin"):
        register_user("admin", "admin", 1)
    while True:
        print("\nLibrary Management System")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            user = login(username, password)
            if user:
                user_id, is_admin = user
                if is_admin:
                    admin_menu(user_id)
                else:
                    user_menu(user_id)
            else:
                print("Invalid credentials.")
        elif choice == '2':
            username = input("Username: ")
            password = input("Password: ")
            if register_user(username, password):
                print("Registered successfully. Please login.")
            else:
                print("Username already exists.")
        elif choice == '3':
            sys.exit(0)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
