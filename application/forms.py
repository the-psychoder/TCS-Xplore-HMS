from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange, InputRequired
from wtforms.fields.html5 import DateField
from datetime import datetime

# Form present in the Login page
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=8, max=10)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField("Sign In")

# Form present in the Create Patient page
class PatCreateForm(FlaskForm):
    ws_ssn          =   IntegerField("SSIN Id :", validators=[InputRequired()])
    ws_pat_name     =   StringField("Name :", validators=[InputRequired(), Length(min=5,max=50, message= "Name length must be minimum of 5")])
    ws_age          =   IntegerField("Age :", validators=[InputRequired(),NumberRange(min=1,max=120, message= "Age must be between 1 to 120")])
    ws_adrs         =   StringField("Address :", validators=[InputRequired(), Length(min=5,max=100, message="Address length must be minimum of 5")])
    ws_doj          =   DateField("Date Of Admission :", format='%Y-%m-%d')
    ws_rtype        =   SelectField("Room type :", choices=[('Single Room','Single Room'),('Semi Room','Semi Room'),('General Room','General Room')])
    state           =   SelectField('State :', choices=[],validate_choice= False)
    city            =   SelectField('City :', choices=[],validate_choice= False)
    submit          =   SubmitField()

    # custom validation
    def validate_ws_ssn(self, ws_ssn):
        if len(str(ws_ssn.data)) != 9:
            raise ValidationError("SSN Id must be of length 9")

    def validate_city(self, city):
        if city.data == None:
            raise ValidationError("This field is empty")
    
    def validate_ws_doj(self, ws_doj):
        diff = ((ws_doj.data) - datetime.now().date()).days
        if diff != 0:
            raise ValidationError("Illegal Date of Admission!!")

# Form present in the Search Patient page
class PatSearchForm(FlaskForm):
    ws_pat_id          =   IntegerField("Patient Id :", validators=[InputRequired()])

    # custom validation
    def validate_ws_pat_id(self, ws_pat_id):
        if len(str(ws_pat_id.data)) != 9:
            raise ValidationError("Id must be of length 9")

# Form present in the Update Patient page
class PatUpdateForm(FlaskForm):
    ws_pat_name     =   StringField("Name :", validators=[InputRequired(), Length(min=5,max=50, message= "Name length must be minimum of 5")])
    ws_age          =   IntegerField("Age :", validators=[InputRequired(),NumberRange(min=1,max=120, message= "Age must be between 1 to 120")])
    ws_adrs         =   StringField("Address :", validators=[InputRequired(), Length(min=5,max=100, message="Address length must be minimum of 5")])
    ws_doj          =   DateField("Date Of Admission :", format='%Y-%m-%d')
    ws_rtype        =   SelectField("Room type :", choices=[('Single Room','Single Room'),('Semi Room','Semi Room'),('General Room','General Room')])
    state           =   SelectField('State :', choices=[],validate_choice= False)
    city            =   SelectField('City :', choices=[],validate_choice= False)
    submit          =   SubmitField('Update')

    # custom validation
    def validate_city(self, city):
        if city.data == None:
            raise ValidationError("This field is empty")
    # Date of Admission relaxation upto 2 days
    def validate_ws_doj(self, ws_doj):
        diff = ((ws_doj.data) - datetime.now().date()).days
        if not((diff >= -2) and (diff <= 2)):
            raise ValidationError("Illegal Date of Admission!!")

# Form present in the Delete Patient page
class PatDelForm(FlaskForm):
    submit          =   SubmitField('Delete')

class IssueMedicineForm(FlaskForm):
    selectMeds    =   SelectField(choices=[])
    qtyMeds       =   IntegerField(validators=[InputRequired()])
    submit        =   SubmitField('Add')

    # custom validation
    def validate_selectMeds(self, selectMeds):
        if selectMeds.data == None:
            raise ValidationError("This field is empty")
