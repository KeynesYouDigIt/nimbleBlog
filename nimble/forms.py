#sign up, login, logout
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import *
from wtforms import ValidationError
from .models import *
from flask.ext.wtf.html5 import URLField


"""custom validators here"""

class Bad_duplicate_email(object):    
    """
    Custom validator I literally just stole from validators.py and customized
    """
    def __init__(self, fieldname, message='somebody already has that email.'):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        message = self.message
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if other.data==False:
            if User.query.filter_by(email=field.data).first():
                field.errors[:] = []
                raise StopValidation(message)


class Match_dick(object):
    """
    Custom validator I literally just stole from validators.py and customized
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        dick=['rock','paper','scissors']
        if field.data not in dick:
            if self.message is None:
                message = field.gettext('not in the dic.')
            else:
                message = self.message
            field.errors[:] = []
            raise StopValidation(message)


class SignupForm(Form):
    username = StringField('username',
                    validators=[
                    DataRequired(), 
                    Length(2,90, message='thats too long or to short. keep it within 2 to 90 chars.\n Dont really know why you want to type that much anyway....'),
                    Regexp('^[A-Za-z0-9_]{2,}',
                        message='stop it with the weird username! must be letters, numbers, and _')
                    ])
    password = PasswordField('password',
                    validators=[
                    DataRequired(),
                    EqualTo('password_confirm',
                        message='slow down there partner, which is it? \n you put something different in password and confirm password...')
                    ])
    password_confirm = PasswordField('confirm password',validators=[DataRequired()])
    doop_email = BooleanField('<font size="1">check here if this email is aready on an account,<br>but you would like to add it to this new one as well</font> &nbsp  &nbsp')
    Email = StringField('Email <font size="1">(optional, but will give you data quicker)</font> &nbsp  &nbsp', 
                    validators=[
                    Optional(),
                    Length(1,120),
                    Bad_duplicate_email('doop_email'),
                    Email(message='dude, valid email. if you dont know what that is google \"email\". or, you know, maybe the internet isn\'t for you?')])

    def validate_username(self,username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('somebody beat you to that username. Common, be original!')



"""forms here"""

class LoginForm(Form):
    username = StringField('Your Username', 
        [InputRequired(message='dude. put something here. anything.')])

    password = PasswordField('Password', 
        [InputRequired(message='dude. put something here. anything.')])

    remember_me = BooleanField('<font size="1">gimmie a cookie to keep me logged in</font> &nbsp  &nbsp')

    submit = SubmitField('Log In')


class DataForm(Form):
    url = StringField('enter url here for the page   _>    ', 
        [InputRequired(message='dude. put something here. anything.')])

    content = TextAreaField('enter your starting content   ')

    tags = StringField('Tag it up! (or dont) <br><em> <font size="1">'+\
        'pick from the list or type a new one to submit it </font></em>&nbsp  &nbsp', 
        validators=[Optional(),Regexp('^[A-Za-z0-9_]{2,}', 
            message='stop it with the weird tag! must be letters, numbers, and _')])

    def validate(self):
        #this overwrites the validate method of the form class
        if not self.url.data.startswith("/"):
            self.url.data = "/" + self.url.data

        if not Form.validate(self):
            return False
            
        stripped=[t.strip() for t in self.tags.data.split(',')]
        legit= [t for t in stripped if t]
        as_set = set(legit)
        self.tags.data = ','.join(as_set)


        return True 