from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.sqlite"

db = SQLAlchemy(app)

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), default="John")
    last_name = db.Column(db.String(30), unique=True)
    cars = db.relationship('Car', backref='ownerbr')

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_plate = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)


@app.route('/')
def home():
    obj1 = Owner.query.filter_by(id=1).first()
    name = obj1.first_name + " " + obj1.last_name
    names = Car.query.all()
    return render_template('index.html', name=name, names=names)

@app.route('/postoption', methods=["GET", "POST"]) 
def posto():
    response = request.method
    return f"Method is {response}"

@app.route('/name/<name>/<int:num>')
def name(name, num):
    var1 = f"{name}<br>" * num
    return var1

@app.route('/gotogoogle')
def gotogoogle():
    return redirect("http://www.google.com")

@app.route('/gotohome')
def gotohome():
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)