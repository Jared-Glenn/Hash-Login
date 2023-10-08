from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField
from wtforms.validators import InputRequired, Optional, AnyOf, URL, NumberRange, Length

class RegisterForm(FlaskForm):
    """Form for adding a new user."""
    
    username = StringField("Username",
                           validators=[Length(max=20, message="Username maximum length is 20 characters.")])
    password = PasswordField("Password")
    email = StringField("Email",
                        validators=[InputRequired(), Length(max=50, message="Email maximum length is 50 characters.")])
    first_name = StringField("First Name",
                             validators=[InputRequired(), Length(max=30, message="Name maximum length is 30 characters.")])
    last_name = StringField("Last Name",
                            validators=[InputRequired(), Length(max=30, message="Name maximum length is 30 characters.")])
    
    
class LoginForm(FlaskForm):
    """Form for adding a new user."""
    
    username = StringField("Username",
                           validators=[Length(max=20, message="Username maximum length is 20 characters.")])
    password = PasswordField("Password")
    

class FeedbackForm(FlaskForm):
    """Form for providing feedback from a specific user."""
    
    title = StringField("Title",
                           validators=[Length(max=100, message="Title maximum length is 100 characters.")])
    content = StringField("Feedback Content")