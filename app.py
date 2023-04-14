from flask import Flask, jsonify, render_template,request, url_for, redirect

import mysql.connector
mydb=mysql.connector.connect(host="database-2.capvgodd0947.eu-north-1.rds.amazonaws.com", user="admin",password="admin123", database="DB")

app = Flask(__name__)


@app.route('/')
def home():
    mycursor=mydb.cursor()
    mycursor.execute("Select * from workers")
    myresult = mycursor.fetchall()

    return render_template('home2.html',data=myresult) 

@app.route('/create/', methods=('GET', 'POST'))
def create():
        mycursor=mydb.cursor()
        sqlform = "Insert into workers(id, name, salary) values(%s,%s,%s)"
        if request.method == 'POST':
            id=request.form['id']
            name = request.form['name']
            salary = request.form['salary']

            worker = [(id,name,salary)]

            mycursor.executemany(sqlform,worker)
            mydb.commit()

            return redirect(url_for('home'))
        return render_template('create.html')

@app.route('/summary')
def summary():
    mycursor=mydb.cursor()
    mycursor.execute("Select * from workers")
    myresult = mycursor.fetchall()

    return render_template('summary.html',data=myresult) 

@app.route('/edit/', methods=('GET', 'POST'))
def edit():
    mycursor=mydb.cursor()
    mycursor.execute("Select * from workers")
    myresult = mycursor.fetchall()
    if request.method == 'POST':
        id=request.form['id']
        name = request.form['name']
        salary = request.form['salary']

        #sql = "UPDATE workers SET salary = "+salary+" WHERE id = "+id+" OR name = "+name
        sql = """UPDATE workers SET salary = '{}' WHERE id = '{}' OR name ='{}'""".format(salary,id,name)

        mycursor.execute(sql)

        mydb.commit()

        return redirect(url_for('home'))

    return render_template('edit.html',data=myresult)



#if __name__ == '__main__':
#    app.run(debug=True)

#from os import environ
#if __name__ == '__main__':
#    HOST = environ.get('SERVER_HOST', 'localhost')
#    try:
#        PORT = int(environ.get('SERVER_PORT', '5555'))
#    except ValueError:
#        PORT = 5555
#    app.run(HOST, PORT)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)
