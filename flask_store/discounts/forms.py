from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Optional
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
    discount_percent = FloatField('Discount Percentage', 
                                  validators=[DataRequired(), NumberRange(min=0, max=100)])
    min_purchase = IntegerField('Minimum Purchase', validators=[Optional()])
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    cancel = SubmitField('Cancel')
    save = SubmitField('Save')

    def validate_code(self, code):
        discount = Discount.query.filter_by(code=code.data).first()
        if discount:
            raise ValidationError('Discount code name is already in use.')