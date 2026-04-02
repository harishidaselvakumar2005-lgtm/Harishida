from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import random
import os
from urllib.parse import urlparse
 
app = Flask(__name__)
 
# 🔥 GET DATABASE URL
db_url = os.getenv("mysql://root:aRlXJXmkESvwdgFbiphPYWDwWZthFhKx@gondola.proxy.rlwy.net:21989/railway")
 
# 👉 fallback for local testing (IMPORTANT)
if not db_url:
    db_url = "mysql://root:aRlXJXmkESvwdgFbiphPYWDwWZthFhKx@gondola.proxy.rlwy.net:21989/railway"
 
url = urlparse(db_url)
 
# 🔥 DATABASE CONNECTION

 

app = Flask(__name__)

# Database Configuration
def get_db_connection():
    return mysql.connector.connect(host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],   # ✅ correct way (remove "/")
    port=url.port)
        

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', customers=customers)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(id) FROM customer")
        result = cursor.fetchone()

        if result[0] is None:
            id = 1
        else:
            id = result[0] + 1

        name = request.form['name']
        mobile = request.form['mobile']
        amount = request.form['amount']
        location = request.form['location']

        cursor.execute(
            "INSERT INTO customer (id, name, mobile, amount, location) VALUES (%s, %s, %s, %s, %s)",
            (id, name, mobile, amount, location)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        mobile = request.form['mobile']
        amount = request.form['amount']
        location = request.form['location']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE customer 
            SET name=%s, mobile=%s, amount=%s, location=%s 
            WHERE id=%s
        """, (name, mobile, amount, location, id_data))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customer WHERE id=%s", (id_data,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)