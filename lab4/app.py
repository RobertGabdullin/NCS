from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              first_name TEXT NOT NULL,
              user_name TEXT NOT NULL,
              password TEXT NOT NULL)''')
conn.commit()
conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user input from form
        first_name = request.form['first_name']
        user_name = request.form['user_name']
        password = request.form['password']

        # Insert user data into SQLite3 database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (first_name, user_name, password) VALUES (?, ?, ?)", (first_name, user_name, password))
        conn.commit()
        conn.close()

        # Redirect to greeting page
        return redirect(url_for('greeting', first_name=first_name))
    return render_template('index.html')

@app.route('/greeting/<first_name>')
def greeting(first_name):
    return render_template('greeting.html', first_name=first_name)

@app.route('/users')
def users():
    # Retrieve all users from SQLite3 database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT user_name FROM users")
    users = c.fetchall()
    conn.close()

    # Render users template with list of usernames
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
