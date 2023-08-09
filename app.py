from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, SubmitField
from flask_testing import TestCase
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.sqlite"
app.config['SECRET_KEY'] = "SECRET_KEY"

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

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

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///testdata.sqlite',
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return app

    def setUp(self):
        db.create_all()

        test_dog = Dog(name='Missy', age=15, breed='pug')
        db.session.add(test_dog)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assertIn('This is the actual page', response.data.decode())

class TestCrud(TestBase):
    def test_dog_form_post(self):
        response = self.client.post(url_for('add_dog'), data = dict(name="Fido", age=7, breed="collie"))
        obj1 = Dog.query.filter_by(name='Fido').first()
        self.assertEqual(obj1.name, 'Fido')

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
    # obj1 = Owner.query.filter_by(id=1).first()
    # name = obj1.first_name + " " + obj1.last_name
    # names = Car.query.all()
    return render_template('index.html')

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