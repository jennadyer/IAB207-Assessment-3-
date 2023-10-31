
from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import InputRequired, Email, EqualTo, NoneOf, NumberRange, Regexp
from flask_wtf.file import FileRequired, FileField, FileAllowed
from datetime import datetime


ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}


# Create new event
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[
                       InputRequired()], render_kw={"placeholder": "Name"})
    location = StringField('Location', validators=[InputRequired()], render_kw={
                           "placeholder": "Location"})
    genre = SelectField(u'Please Select a Genre that Best Describes Your Event', choices=[
                        'Genre', 'Pop', 'Rock', 'Rap', 'Classical', 'Jazz', 'Country'], validators=[NoneOf('Genre', 'Please select a genre.')])
    start_date = DateField('Start Date', validators=[InputRequired()])
    start_time = TimeField('Start Time', validators=[InputRequired()])
    end_date = DateField('End Date', validators=[InputRequired()])
    end_time = TimeField('End Time', validators=[InputRequired()])
    total_tickets = IntegerField('Tickets Available', validators=[
                                 InputRequired(), NumberRange(min=20, message='Minimum ticket requirement is 20')], render_kw={"placeholder": "20"})
    price = StringField("Price (Please enter price in $10.00 format)", validators=[Regexp(
        r"([0-9]+.[0-9][0-9])", message="Please enter a valid price.")], render_kw={"placeholder": "10.00"})
    description = TextAreaField('Description',
                                validators=[InputRequired()], render_kw={"placeholder": "Enter a description of event."})
    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])

    submit = SubmitField("Submit")

    # Custom validation function for date fields (redefine built-in)
    def validate(self, **kwargs):
        # Standard validators
        validators = FlaskForm.validate(self)
        # Ensure all standard validators are met
        if validators:
            # Ensure end date >= start date
            if (self.start_date.data > self.end_date.data):
                self.end_date.errors.append(
                    'Finish date must be set after the starting date.')
                return False
            if self.start_date.data <= datetime.date(datetime.now()):
                print("start error")
                self.start_date.errors.append(
                    'Date is passed.')
                return False
            if self.end_date.data <= datetime.date(datetime.now()):
                print("end error")
                self.end_date.errors.append(
                    'Date is passed.')
                return False
            if self.start_time.data >= self.end_time.data:
                if self.start_date.data == self.end_date.data:
                    print("test")
                    self.end_time.errors.append(
                        'Finish time must be set after the starting time.')
                    return False

            return True

        return False


class UpdateForm(FlaskForm):
    cancel = BooleanField('Cancel Event')
    name = StringField('Event Name', validators=[
                       InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    genre = SelectField(u'Please Select a Genre that Best Describes Your Event', choices=[
                        'Genre', 'Pop', 'Rock', 'Rap', 'Classical', 'Jazz', 'Country'], validators=[NoneOf('Genre', 'Please select a genre.')])
    start_date = DateField('Start Date', validators=[InputRequired()])
    start_time = TimeField('Start Time', validators=[InputRequired()])
    end_date = DateField('End Date', validators=[InputRequired()])
    end_time = TimeField('End Time', validators=[InputRequired()])
    total_tickets = IntegerField('Tickets Available', validators=[
                                 InputRequired(), NumberRange(min=1, message='Tickets available cannot be less than 1.')])
    price = StringField("Price (Please enter price in $10.00 format)", validators=[Regexp(
        r"([0-9]+.[0-9][0-9])", message="Please enter a valid price.")])
    description = TextAreaField('Description',
                                validators=[InputRequired()])
    image = FileField('Event Image (Leave blank to use previously saved image.)', validators=[FileAllowed(
        ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])

    submit = SubmitField("Update")

    # Custom validation function for date fields (redefine built-in)
    def validate(self, **kwargs):
        # Standard validators
        validators = FlaskForm.validate(self)
        # Ensure all standard validators are met
        if validators:
            print("test 1")
            # Ensure end date >= start date
            if (self.start_date.data > self.end_date.data):
                self.end_date.errors.append(
                    'Finish date must be set after the starting date.')
                self.start_date.errors.append(
                    'Finish date must be set after the starting date.')
                print("test val")
                return False
            if self.start_date.data <= datetime.date(datetime.now()):
                print("start error")
                self.start_date.errors.append(
                    'Date is passed.')
                return False
            if self.end_date.data <= datetime.date(datetime.now()):
                print("end error")
                self.end_date.errors.append(
                    'Date is passed.')
                return False
            if self.start_time.data >= self.end_time.data:
                if self.start_date.data == self.end_date.data:
                    print("test")
                    self.end_time.errors.append(
                        'Finish time must be set after the starting time.')
                    return False

            return True

        return False


# Create booking
class BookingForm(FlaskForm):
    num_tickets = IntegerField(
        'Select number of tickets', validators=[InputRequired(), NumberRange(min=1, message='Minimum tickets is 1')])
    submit = SubmitField('Buy Now')

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
    phone_id = StringField("Phone Number", validators=[Regexp(
        r"([0-9]+)", message="Please enter a valid phone number.")])
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")


# User comment
class CommentForm(FlaskForm):
    text = TextAreaField('', [InputRequired()])
    submit = SubmitField('Create')
