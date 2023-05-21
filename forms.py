from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class SignupForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    account = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    account = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()
