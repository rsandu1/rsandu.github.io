from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

conn = sql.connect('database.db')
print("Opened database successfully");

conn.execute('CREATE TABLE IF NOT EXISTS comments (name TEXT, comment TEXT)')
print("Table created successfully");
conn.close()

@app.route('/')
def hello_world():
   return render_template('index.html')

@app.route('/enternew/')
def new_student():
   return render_template('comment.html')

@app.route('/addrec/',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         com = request.form['com']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO comments (name,comment) VALUES (?,?)",(nm,com) )
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "Error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list/')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from comments")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run()