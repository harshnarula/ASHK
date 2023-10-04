from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from flask_login import current_user
from wtforms import StringField , TextField ,PasswordField ,SubmitField , BooleanField , SelectField , DateField , IntegerField ,TextAreaField
from wtforms.validators import DataRequired , Length , EqualTo , ValidationError
from managment.datbase import User



class redistrationform(FlaskForm):
    fn = StringField('First Name :' , validators=[DataRequired() , Length(min = 4, max=10)])
    mn = StringField('Middle Name :' , validators=[DataRequired() , Length(min = 4, max=10)])
    ln = StringField('last Name :' , validators=[DataRequired() , Length(min = 4, max=10)])
    email = StringField('Email :',validators=[DataRequired() ])
    user_type =StringField('use type :',validators=[DataRequired()])
    password = PasswordField('Password :' , validators=[DataRequired() , Length(min=8 ,max=15)])
    cnfpass = PasswordField('Confirm Password' , validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    

    def validate_email(self , email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('The email is already been Used, Pleace Choose Different Email or login With the Email')


class loginform(FlaskForm):
    email = StringField('Email :',validators=[DataRequired()])
    password = PasswordField('Password :' , validators=[DataRequired() , Length(min=8 ,max=15)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')




class Accountform(FlaskForm):
    fn = StringField('First Name :' , validators=[DataRequired() , Length(min = 4, max=10)])
    mn = StringField('Middle Name :' , validators=[DataRequired() , Length(min = 4, max=10)])
    ln = StringField('last Name :' , validators=[DataRequired() , Length(min = 4, max=10)])
    email = StringField('Email :',validators=[DataRequired()])
    picture = FileField('Update Profile Picture' , validators=[FileAllowed(['jpg' , 'png'])])
    add1 = StringField('Address line 1 :',validators=[DataRequired()])
    add2 = StringField('Address line 2 :',validators=[DataRequired()])
    add3 = StringField('Address line 3 :',validators=[DataRequired()])
    add4 = StringField('Address line 4 :',validators=[DataRequired()])
    add5 = StringField('State :',validators=[DataRequired()])
    add6 = StringField('city :',validators=[DataRequired()])
    pincode = IntegerField('Pincode :',validators=[DataRequired()])
    submit = SubmitField('Update')
    

    def validate_email(self , email):
        if current_user.email != email.data:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('The email is already been Used, Pleace Choose Different Email or login With the Email')


class tourform(FlaskForm):
    place = SelectField('Place of Journey :' ,choices =[('Hydrabad'),('Delhi'),('New York')] , validators=[DataRequired() , Length(min = 4, max=10)])
    doj = DateField('Date Of Journey :' , format='%Y-%m-%d' , validators=[DataRequired()])
    nop = IntegerField('Number Of Traveler :' , validators=[DataRequired()])
    package_amt = IntegerField('Amount Per Person :' , validators=[DataRequired()])
    total_amt = IntegerField('Total Amount :' , validators=[DataRequired()])
    submit = SubmitField('Confirm')


class reviewform(FlaskForm):
    title =  StringField('Package :' ,validators=[DataRequired()] )
    review = TextAreaField('Review :' , validators=[DataRequired()])
    submit = SubmitField('Submit')
