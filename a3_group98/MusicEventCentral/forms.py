
from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed


ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}


# Create new event
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    # genre
    start_date = DateField('Start Date', validators=[InputRequired()])
    start_time = TimeField('Start Time', validators=[InputRequired()])
    end_date = DateField('End Date', validators=[InputRequired()])
    end_time = TimeField('End Time', validators=[InputRequired()])
    total_tickets = IntegerField(
        'Tickets Available', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    description = TextAreaField('Description',
                                validators=[InputRequired()])
    image = FileField('Destination Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    submit = SubmitField("Submit")


# creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form


class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
                           Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")


class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')
