from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from flask_store.discounts.models import Discount

class DiscountForm(FlaskForm):
    name = StringField('Discount Name', validators=[DataRequired(), Length(min=5, max=100)])
    code = StringField('Discount Code', validators=[DataRequired(), Length(min=5, max=50)])
    description = TextAreaField('Discount Description', validators=[DataRequired()])
    type = SelectField('Discount Type', 
                        choices=[
                            ('', 'Select Discount Type'),
                            ('shipping', 'Shipping Discount'), # ('value stored in db', 'front-end label')
                            ('seasoning', 'Seasonal Discount'),
                            ('special_event', 'Special Event')
                        ],
                        validators=[DataRequired()])
    discount_percent = FloatField('Discount Percentage (0-1)', 
                                  validators=[DataRequired(), NumberRange(min=0, max=1)])
    cancel = SubmitField('Cancel')
    save = SubmitField('Save')

    def validate_code(self, code):
        discount = Discount.query.filter_by(code=code.data).first()
        if discount:
            raise ValidationError('Discount code name is already in use.')