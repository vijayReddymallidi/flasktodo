from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__,static_folder="./static")


conn = sqlite3.connect('todo.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY NOT NULL  , task TEXT NOT NULL , description TEXT NOT NULL )''')
conn.commit()
conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    # print(tasks)
    conn.close()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    description = request.form['description']
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, description) VALUES (?, ?)", (task, description))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete_task(id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
@app.route('/edit/<int:id>')
def edit_task(id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = c.fetchone()
    # print(task)
    conn.close()
    return render_template('edit.html', task=task)

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    task = request.form['task']
    description = request.form['description']
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET task=?, description=? WHERE id=?", (task, description, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
