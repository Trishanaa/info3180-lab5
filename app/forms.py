# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm 
from wtforms import StringField,TextAreaField,FileField
from wtforms.validators import DataRequired,Length
from flask_wtf.file import FileAllowed


class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    poster = FileField('Movie Poster', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])