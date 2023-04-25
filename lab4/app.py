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

def F(string):
    return ''.join(filter(str.isalnum, string))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        user_name = request.form['user_name']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (first_name, user_name, password) VALUES (?, ?, ?)", (first_name, user_name, password))
        conn.commit()
        conn.close()

        return redirect(url_for('greeting', first_name=F(first_name), real_name = first_name))
    return render_template('index.html')

@app.route('/greeting/<first_name>')
def greeting(first_name):
    return render_template('greeting.html', first_name=request.args.get('real_name', ''))
    #return '<html><body> <h1> Hello ' + request.args.get('real_name', '') + '</h1> <a href="/users">View all users</a> !</body></html>'

@app.route('/users')
def users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT user_name FROM users")
    users = c.fetchall()
    conn.close()

    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
