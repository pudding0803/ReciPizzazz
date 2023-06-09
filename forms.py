from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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


class RecipeForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    ingredients = StringField(validators=[DataRequired()])
    instructions = CKEditorField(validators=[DataRequired()])
    public = BooleanField(default=True)
    submit = SubmitField()
