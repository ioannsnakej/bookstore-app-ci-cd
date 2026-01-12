from flask import Flask, render_template, jsonify, request, flash, redirect
from db import get_connection
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secretkey')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books ORDER BY author, title')
        books = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('books.html', books=books)
    except Exception as e:
        flash(f'Ошибка подключения к базе: {str(e)}', 'error')
        return render_template('books.html', books=[])

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        try:
            title = request.form['title']
            author = request.form['author']
            price = request.form['price']
            count = request.form['count']
        
            conn = get_connection()
            cur = conn.cursor()
                    
            cur.execute(
                'INSERT INTO books (title, author, price, count) VALUES (%s, %s, %s, %s)',
                (title, author, price, count)
            )
                
            conn.commit()
            cur.close()
            conn.close()
                    
            flash('Книга успешно добавлена!', 'success')
            return redirect('/books')
                
        except Exception as e:
            flash(f'Ошибка при добавлении книги: {str(e)}', 'error')
            return render_template('create.html')
    
    else:
        return render_template('create.html')

@app.route('/edit', defaults={'id': None})
@app.route('/edit/', defaults={'id': None})
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if id is None:
        flash('Для редактирования укажите ID книги', 'error')
        return redirect('/books')
    if request.method == "POST":
        # Обработка формы редактирования
        try:
            title = request.form['title']
            author = request.form['author']
            price = float(request.form['price'])
            count = int(request.form['count'])
            
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                'UPDATE books SET title = %s, author = %s, price = %s, count = %s WHERE id = %s',
                (title, author, price, count, id)
            )
            conn.commit()
            cur.close()
            conn.close()
            
            flash('Книга успешно обновлена!', 'success')
            return redirect('/books')
            
        except Exception as e:
            flash(f'Ошибка при обновлении книги: {str(e)}', 'error')
            return redirect(f'/edit/{id}')
    
    else:
        # GET запрос - показ формы редактирования
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM books WHERE id = %s', (id,))
            book = cur.fetchone()
            cur.close()
            conn.close()
            
            if book:
                return render_template('edit.html', book=book)
            else:
                flash('Книга не найдена', 'error')
                return redirect('/books')
                
        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'error')
            return redirect('/books')

@app.route('/delete', defaults={'id': None})
@app.route('/delete/', defaults={'id': None})
@app.route('/delete/<int:id>')
def delete(id):
    if id is None:
        flash('Для удаления укажите ID книги', 'error')
        return redirect('/books')
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Получаем название книги для сообщения
        cur.execute('SELECT title FROM books WHERE id = %s', (id,))
        book_title = cur.fetchone()[0]
        
        cur.execute('DELETE FROM books WHERE id = %s', (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        flash(f'Книга "{book_title}" успешно удалена!', 'success')
        
    except Exception as e:
        flash(f'Ошибка при удалении: {str(e)}', 'error')
    
    return redirect('/books')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
