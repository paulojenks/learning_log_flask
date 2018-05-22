from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, DateField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    date = DateField('Date', validators=[DataRequired()])
    time_spent = StringField('Time Spent', validators=[DataRequired()])
    what_i_learned = TextAreaField('What I learned', validators=[DataRequired(), Length(max=1000)])
    resources_to_remember = TextAreaField('Resources to remember', validators=[DataRequired(), Length(max=1000)])