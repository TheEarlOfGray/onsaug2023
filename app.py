from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, SubmitField
import os

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.sqlite"
app.config['SECRET_KEY'] = "SECRET_KEY"

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

class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    breed = db.Column(db.String)


class DogForm(FlaskForm):
    name = StringField("Name: ")
    age = IntegerField("Age: ")
    breed = SelectField("Breed: ", choices=[
        ("collie", "Collie"),
        ("retriever", "Retriever"),
        ("pug", "Pug")
    ])
    submit = SubmitField("Submit")

@app.route('/add-dog', methods=['GET', 'POST'])
def add_dog():
    form = DogForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            dog = Dog(
                name = form.name.data,
                age = form.age.data,
                breed = form.breed.data
            )
            db.session.add(dog)
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('add_dog.html', form=form)

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