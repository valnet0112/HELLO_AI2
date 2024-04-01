from flask import Flask
from flask.globals import request
from flask.templating import render_template
import pymysql

from day01.daoemp import DaoEmp
from day01.daodiet import DaoDiet
from day01.daomenu import DaoMenu

de = DaoEmp()
dd = DaoDiet()
dm = DaoMenu()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/emp')
def emp():
    emps = de.selectList()
    return render_template('emp.html', emps=emps)

@app.route('/diet')
def diet():
    list = dd.dietList()
    return render_template('diet.html', list=list)

@app.route('/menu')
def menu():
    list = dm.menuList()
    return render_template('menu.html', list=list)

@app.route('/recom')
def recom():
    return render_template('recom.html')


if __name__ == '__main__':
    app.run(debug=True)