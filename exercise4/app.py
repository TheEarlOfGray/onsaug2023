from typing import Any
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length

app = Flask(__name__)

app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

class BasicForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=30)
    ])
    last_name = StringField('Last Name')
    dob = DateField('Date of Birth')
    fav_num = IntegerField('Favourite Number')
    fav_food = SelectField('Favourite Food', choices=[
        ('pizza', 'Pizza'),
        ('spaghetti', 'Spaghetti'),
        ('chilli', 'Chilli')
    ])
    username = StringField('Username')
    submit = SubmitField('Add Name')

    # def validate_username(self, username):
    #     if username.data.lower() == 'admin':
    #         raise ValidationError("Can't use admin as a username! Try again.")
        
# class checkAdmin:
#     def __init__(self, message=None):
#         if not message:
#             message = 'Please choose another username.'
#         self.message = message

#     def __call__(self, form, field):
#         if field.data.lower() == 'admin':
#             raise ValidationError(self.message)
        

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def register():
    message = ""
    form = BasicForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            fav_num = form.fav_num.data
            fav_food = form.fav_food.data

            if len(first_name) == 0 or len(last_name) == 0:
                message = "Please supply both first and last name"
            else:
                message = f'Thank you, {first_name} {last_name}. I hope your day contains {fav_num} {fav_food}.'

    return render_template('home.html', form=form, message=message)

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0')