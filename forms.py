from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , BooleanField,PasswordField, ValidationError, TextAreaField,FileField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired , EqualTo, Length
from flask_ckeditor import CKEditorField

class Searchform(FlaskForm):
    searched = StringField("Searched",validators=[DataRequired()])
    submit = SubmitField("Submit")

class Loginform(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])
    submit = SubmitField("Submit")

class postForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField('content', validators=[DataRequired()])
    #content = StringField("Content", validators=[DataRequired()],widget=TextArea())
    author =StringField("Author")
    slug =StringField("Slug", validators=[DataRequired()])
    submit =SubmitField("Submit", validators=[DataRequired()])

class userForm(FlaskForm):
    name = StringField("Name ",validators=[DataRequired()])
    username=StringField("User name ",validators=[DataRequired()])
    email = StringField("Email ",validators=[DataRequired()])
    fav_color=StringField("Favorite Color")
    about_author = TextAreaField("About Author ")
    profilepic = FileField("Profile picture ")
    password_hash = PasswordField('Password',validators=[DataRequired(),EqualTo('password_hash2',message='Password Must match confirm Password...')])
    password_hash2 = PasswordField('Confirm password',validators=[DataRequired()])
    submit = SubmitField("Submit")

#create a name form flask
class NameForm(FlaskForm):
    name = StringField("Whats your name",validators=[DataRequired()])
    submit = SubmitField("Submit")

#create a password form flask
class PasswordForm(FlaskForm):
    email = StringField("Whats your Email",validators=[DataRequired()])
    password_hash = PasswordField("Whats your password",validators=[DataRequired()])
    submit = SubmitField("Submit")



