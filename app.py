from flask import Flask,request,render_template,redirect,flash,url_for
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)
app.secret_key = "CRISPR-CAS"
mysql = MySQL()

#mysql Configuration

app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='python_sql'
app.config['MYSQL_DATABASE_host']='localhost'
mysql.init_app(app)

@app.route('/')
def Index():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('select * from cities')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html',cities = data)

@app.route('/add_cities',methods=['POST'])
def add_cities():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        name = request.form['cityname']
        population = request.form['population']
        print(name)
        cur.execute('INSERT INTO cities (name,population) VALUES (%s,%s)',(name,population))
        conn.commit()
        flash('city added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>',methods = ['POST','GET'])
def get_cities(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("select * from cities WHERE id = %s",(id))

    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html',cities = data[0])

@app.route('/update/<id>',methods=['POST'])
def update_cities(id):
    if request.method=='POST':
        name = request.form['cityname']
        population = request.form['population']
        conn = mysql.connect()
        cur = conn.cursor()
        query = """UPDATE cities SET name = %s,population = %s WHERE id = %s"""
        data = (name,population,id)
        cur.execute(query,data)
        conn.commit()
        flash("contact updated successfuly")
        conn.close()
        return redirect(url_for('Index'))

@app.route('/delete/<id>',methods =['POST','GET'])
def delete_cities(id):
    if request.method=='POST' or 'GET':
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM cities WHERE id = %s",(id))
        conn.commit()
        flash("City removed successfully")
        conn.close()
        return redirect(url_for('Index'))



#Starting the app
if __name__ == "__main__":
    app.run(port=3000,debug=True)