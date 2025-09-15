Library Management System

(https://youtu.be/Qpq4AW8HfEI)

(https://youtu.be/Qpq4AW8HfEI?si=FWWkLyELzLrjpHlm)
[Link to YouTube video demonstration]

Description

The Library Management System is a console-based Python application that enables efficient management of a library's books and users. Built using SQLite for persistent storage, it provides distinct interfaces for administrators and regular users. Admins can add books, manage user accounts, issue and return books, while users can search for books, view available books, and check their issued books. This project fulfills the CS50 Python final project requirements by implementing a robust system with custom functions, automated tests, and clear documentation.

Background

Libraries require organized systems to track books, manage user borrowings, and maintain records. Manual processes can be time-consuming and error-prone. This digital solution streamlines these tasks, offering a user-friendly interface for both library staff (admins) and patrons (users). The project demonstrates proficiency in Python programming, database management, user authentication, and error handling, building on concepts learned in CS50's Python course.

Features
User Management:
Register new users with a username and password.
Authenticate users and admins via login.

Book Management:
Add new books with title, author, and publication year.
Search books by title or author using keywords.
List all books with their status (available or issued).

Book Borrowing:
Issue books to users (admin-only).
Return issued books (admin-only).
View issued books for a specific user.

Role-Based Access:
Admin interface for managing books and users.
User interface for browsing and checking issued books.

Persistent Storage: Uses SQLite to store users, books, and borrowing records.
Error Handling: Validates inputs and handles database errors gracefully.

How It Works
Run python project.py to start the program.
Choose to:

Login: Use admin/admin for admin access or register a new user.
Register: Create a new user account with a unique username.
Exit: Close the program.
Admin Menu:
Add books, issue/return books, register new users, list/search books.
User Menu:
View all books, search books, or check issued books.
Data is stored in library.db, created automatically on first run.
Implementation Details

Technology Stack:
Python: Core language for logic and user interface.
SQLite: Lightweight database for storing users, books, and issued books.
Standard Library: Uses sqlite3 for database operations and sys for program exit.

Database Schema:
users: Stores user_id, username, password, and is_admin (1 for admin, 0 for user).
books: Stores book_id, title, author, year, and status (available or issued).
issued_books: Tracks issue_id, user_id, book_id, and issue_date.

Custom Functions:
add_book(title, author, year): Adds a new book to the database.
search_books(keyword): Searches books by title or author.
issue_book(user_id, book_id): Issues a book to a user if available.
Testing:
test_project.py includes three test functions: test_add_book, test_search_books, and test_issue_book.
Tests verify book addition, search functionality, and book issuing/returning using pytest.
Challenges:
Ensuring database integrity (e.g., preventing duplicate usernames or issuing unavailable books).
Designing a clear menu-driven interface for both admins and users.
Writing robust tests to cover edge cases, such as invalid inputs or non-existent books.
Effort exceeded individual problem sets due to database design, user role management, and test implementation.
