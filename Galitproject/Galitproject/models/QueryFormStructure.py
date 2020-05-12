
from flask_wtf import FlaskForm
from wtforms import Form, PasswordField, SelectMultipleField, StringField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired
### ----------------------------------------------------------- ###



class QueryFormStructure(FlaskForm):
    name   = StringField('Year :  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')




class LoginFormStructure(FlaskForm):
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')




class UserRegistrationFormStructure(FlaskForm):
    FirstName  = StringField('First name:  ' , validators = [DataRequired()])
    LastName   = StringField('Last name:  ' , validators = [DataRequired()])
    PhoneNum   = StringField('Phone number:  ' , validators = [DataRequired()])
    EmailAddr  = StringField('E-Mail:  ' , validators = [DataRequired()])
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')

class olimform(FlaskForm):
    
    years = SelectMultipleField('Select Multiple Year:' , validators = [DataRequired] )
    submit = SubmitField('submit')






