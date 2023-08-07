from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create connection object
conn = sqlite3.connect('expenses.db')
# Create cursor object
cur = conn.cursor()
# Execute query
cur.execute(''' CREATE TABLE IF NOT EXISTS sitt (
subject TEXT,
date TEXT,
cost REAL,
PRIMARY KEY (subject,date));''')
# Commit to disk
conn.commit()
# Close connection
conn.close()

@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == "POST":
    subject = request.form['subject']
    cost = request.form['cost']
    date = request.form['date']
    # Create connection object
    conn = sqlite3.connect("expenses.db")
    # Create cursor
    cur = conn.cursor()
    # Execute query
    # For removing test data
    # cur.execute("DELETE FROM sitt;")
    # conn.commit()
    cur.execute("INSERT INTO sitt (subject, date, cost) VALUES (?,?,?);",(subject, date, cost))
    # Commit to disk
    conn.commit()
    # Get records
    # cur.execute('SELECT * FROM sitt;')
    cur.execute('SELECT subject, SUM(cost) AS total FROM sitt GROUP BY subject ORDER BY total DESC;')
    records = cur.fetchall()
    cur.execute('SELECT * FROM sitt')
    rows = cur.fetchall()
    # Close connection
    conn.close()
    
    return render_template('index.html', subject=subject, cost=cost, date=date, records=records, rows=rows)
  return render_template('index.html')
    


app.run(host='0.0.0.0', port=81)
