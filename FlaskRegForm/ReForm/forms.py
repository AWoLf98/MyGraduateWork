from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    cPassword = PasswordField('Comfirm Password', validators=[DataRequired()])

    agreeSubmit = SubmitField('Zimbra')
    errorSubmit = SubmitField('Continue')

    agreeVer = BooleanField()
    submit = SubmitField('Register')
