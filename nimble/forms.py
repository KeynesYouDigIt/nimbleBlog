"""This file creates classes, 
which are passed to the router in views.py as displayable objects passed 
to Jinja for rendering."""

from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, \
BooleanField, SubmitField, TextAreaField
from wtforms.validators import *
from wtforms import ValidationError
from .models import *
from wtforms.fields.html5 import URLField

class SignupForm(Form):
    """typical user registration form.
    username must be 2-90 characters in length with no specials, unique.

    password only has to match confirm password.

    email is strictly optional, can be used for multiple accounts. 
    This is because the site proritizes flexibility and anonymnity over 
    saftey or user workflow control """

    username = StringField('username&nbsp',
                    validators=[
                        DataRequired(), 
                        Length(2,80, \
                            message='thats too long or to short. keep it within 2 to 80 chars.'+\
                            '\n Dont really know why you want to type that much anyway....'),
                        Regexp('^[A-Za-z0-9_]{2,}',
                        message='stop it with the weird username!'+\
                        'must be letters, numbers, and _')
                    ])
    password = PasswordField('password',
                    validators=[
                    DataRequired(),
                    EqualTo('password_confirm',
                        message='slow down there partner, which is it?\n '+\
                        'you put something different in \'password\' and'+\
                        ' \'confirm password\'...')
                    ])
    password_confirm = PasswordField('confirm password&nbsp',
                    validators=[DataRequired()
                    ])
    Email = StringField('Email <font size="1">(optional)</font> &nbsp  &nbsp', 
                    validators = [
                    Optional(),
                    Length(1,120),
                    Email(message='dude, valid email please.')])

    def validate_username(self,username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('somebody beat you to that username.'+\
                'Common, be original!')


class LoginForm(Form):
    """typical login  form.
    remember_me boolean sends a cookie to keep the login session for 
    500 days or until cookies are cleared. """

    username = StringField('Username &nbsp', 
        [InputRequired(message='dude. put something here. anything.')])

    password = PasswordField('Password &nbsp', 
        [InputRequired(message='dude. put something here. anything.')])

    remember_me = BooleanField('<font size="1">gimmie a cookie to keep me logged in</font> &nbsp  &nbsp', default = True)

    submit = SubmitField('Log In')


class DataForm(Form):
    """This form allows for both creation and editing of posts.
    url will be like the name of the post with a '/' added for easy routing
    and a web aesthetic when displayed.

    content is an open text field containing the content of the post 
    with no restrictions (wtforms escapes html).

    tags are the main workflow step for viewing other user's posts, 
    no special characters allowed. They are comma seperated when entered.

    The last few lines in validation 
    prevent seperate records for the same tag. 
    """
    url = StringField('enter the name here for the post   _> &nbsp', 
        [InputRequired(message='dude. put something here. anything.')])

    content = TextAreaField('enter your starting content   ')

    tags = StringField('Tag it up! (or dont) <br><br>'+\
        'seperate each tag with a comma<br><br>'+\
        '<em> <font size="1">'+\
        'pick from the list or type a new one to submit it'+\
        '</font></em>&nbsp  &nbsp', 
        validators = [
            Length(2,25, \
            message='thats too long. keep it within 25 chars.'),
            Optional(),
            Regexp('^[A-Za-z0-9_]{2,}', 
            message='tags must be letters, numbers, and _s')])

    def validate(self):
        #this overwrites the validate method of the form class
        if not self.url.data.startswith("/"):
            self.url.data = "/" + self.url.data

        if not Form.validate(self):
            return False
            
        stripped = [t.strip() for t in self.tags.data.split(',')]
        legit = [t for t in stripped if t]
        as_set = set(legit)
        self.tags.data = ','.join(as_set)


        return True 