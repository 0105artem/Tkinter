#! python3
# backend for the frontend.py file

import sqlite3

class Database():
    def __init__(self, db):
        self.conn = sqlite3.connect('books.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title text, author text,\
            year integer, isbn integer)")
        self.conn.commit()


    def insert(self, title, author, year, isbn):
        self.cur.execute("INSERT INTO book VALUES (NULL, ?, ?, ?, ?)", (title, author, year, isbn))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM book")
        rows = self.cur.fetchall()
        return rows


    def search(self, title="", author="", year="", isbn=""):
        # Searching for an entry based on what the user has entered (16 cases:
        # (title, author, year and isbn) or only (title) or only (author) and so on)
        if title:
            if author:
                if year:
                    if isbn:
                        self.cur.execute("SELECT * FROM book WHERE title=? and author=? and year=? and isbn=?", (title, author, year, isbn)) # title, author, year and isbn
                    else:
                        self.cur.execute("SELECT * FROM book WHERE title=? and author=? and year=?", (title, author, year)) # title, author and year
                elif isbn:
                    self.cur.execute("SELECT * FROM book WHERE title=? and author=? and isbn=?", (title, author, isbn)) #title, author and isbn
                else:
                    self.cur.execute("SELECT * FROM book WHERE title=? and author=?", (title, author)) # title and author
            elif year:
                if isbn:
                    self.cur.execute("SELECT * FROM book WHERE title=? and year=? and isbn=?", (title, year, isbn)) # title, year and isbn
                else:
                    self.cur.execute("SELECT * FROM book WHERE title=? and year=?", (title, year)) # title and year
            elif isbn:
                self.cur.execute("SELECT * FROM book WHERE title=? and isbn=?", (title, isbn)) # title and isbn
            else:
                self.cur.execute("SELECT * FROM book WHERE title=?", (title,)) # title
        elif author:
            if year:
                if isbn:
                    self.cur.execute("SELECT * FROM book WHERE author=? and year=? and isbn=?", (author, year, isbn)) # author, year and isbn
                else:
                    self.cur.execute("SELECT * FROM book WHERE author=? and year=?", (author, year)) # author and year
            elif isbn:
                self.cur.execute("SELECT * FROM book WHERE author=? and isbn=?", (author, isbn)) # author and isbn
            else:
                self.cur.execute("SELECT * FROM book WHERE author=?", (author,)) #author
        elif year:
            if isbn:
                self.cur.execute("SELECT * FROM book WHERE year=? and isbn=?", (year, isbn)) # year and isbn
            else:
                self.cur.execute("SELECT * FROM book WHERE year=?", (year,)) # year
        elif isbn:
            self.cur.execute("SELECT * FROM book WHERE isbn=?", (isbn,)) # isbn
        rows = self.cur.fetchall()
        return rows


    def delete(self, id):
        self.cur.execute("DELETE FROM book WHERE id=?", (id,))
        self.conn.commit()


    def update(self, id, title, author, year, isbn):
        self.cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, id))
        self.conn.commit()


    def __del__(self):
        self.conn.close()
