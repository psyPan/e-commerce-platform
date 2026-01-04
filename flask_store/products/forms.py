from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileAllowed, FileField, FileRequired

class ProductForm(FlaskForm):
    name = StringField('Product Name',  validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Product Description')
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png'])])
    buy_price = IntegerField('Buying Price', validators=[DataRequired(), NumberRange(min=1, message='Price cannot be negative')])
    sell_price = IntegerField('Selling Price', validators=[DataRequired(), NumberRange(min=1, message='Price cannot be negative')])
    stock = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0, message='In stock quantity cannot be negative value')])
    manufacturer = StringField('Manufacturer', validators=[Length(min=3, max=100)])
    type = SelectField('Product Type', 
                        choices=[
                            ('', 'Select Product Type'),
                            ('laptop', 'Laptop'),
                            ('phone', 'Phone'),
                            ('tablet', 'Tablet'),
                            ('gaming console', 'Gaming Console'),
                            ('home appliance', 'Home Appliance')
                        ])
    model = StringField('Model', validators=[Length(min=5, max=100)])
    # discount_code = StringField('Discount Code', validators=[Length(min=5, max=50)])
    discount_code = SelectField('Discount Code', choices=[])
    save = SubmitField('Save')