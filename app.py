import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = "books.db"

def connectdb():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connectdb()
    conn.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    judul VARCHAR(100) NOT NULL,
                    penulis VARCHAR(100) NOT NULL
                );''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = connectdb()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']
        conn = connectdb()
        conn.execute("INSERT INTO books (judul, penulis) VALUES (?, ?)", (judul, penulis))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = connectdb()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()
    if not book:
        return "Buku tidak ditemukan", 404

    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']
        conn.execute("UPDATE books SET judul = ?, penulis = ? WHERE id = ?", (judul, penulis, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', book=book)

@app.route('/delete/<int:id>')
def delete(id):
    conn = connectdb()
    conn.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=6001, debug=True)