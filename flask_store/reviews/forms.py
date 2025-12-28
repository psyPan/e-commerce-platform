from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

class ReviewForm(FlaskForm):
    stars = SelectField('Rating', choices=[
        ('5', '5 Stars - Excellent'),
        ('4', '4 Stars - Good'),
        ('3', '3 Stars - Average'),
        ('2', '2 Stars - Poor'),
        ('1', '1 Star - Terrible')
    ], validators=[DataRequired()])
    
    description = TextAreaField('Review', validators=[
        DataRequired(), 
        Length(min=5, max=500, message="Review must be between 5 and 500 characters.")
    ])
    
    submit = SubmitField('Submit Review')