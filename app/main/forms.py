from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, TextAreaField, SubmitField,IntegerField
from wtforms.validators import Required,Email


class EventForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    category = SelectField('Category', choices=[('Food','Food'),('Clothes','Clothes'),('Money','Money'),('Books','Books')],validators=[Required()])
    description = TextAreaField('Your event description', validators=[Required()])
    value = IntegerField('Amount need for event', validators=[Required()])
    event_pic_path = StringField('Upload image url')
    submit = SubmitField('Save')


class DonorForm(FlaskForm):
    name = StringField('Your name', validators=[Required()])
    email = StringField('Your Email Address',validators=[Required(),Email()])
    value = IntegerField('Amount donated', validators=[Required()])
    submit = SubmitField('Donate')    