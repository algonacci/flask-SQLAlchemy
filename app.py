from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)
print('Database Connected!')

class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(15))

    def __init__(self, name, city, address, phone_number):
        self.name = name
        self.city = city
        self.address = address
        self.phone_number = phone_number

@app.route('/')
def index():
    return render_template('index.html', students=Students.query.all())

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['address'] or not request.form['phone_number']:
            flash('Please enter all the fields', 'error')
        else:
            student = Students(request.form['name'], request.form['city'], request.form['address'], request.form['phone_number'])
            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('index'))
    return render_template('add.html')