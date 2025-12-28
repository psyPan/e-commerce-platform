import secrets
import os
from flask import current_app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_f_name = random_hex + f_ext
    
    # Create directory if it doesn't exist
    upload_folder = os.path.join(current_app.root_path, 'static/product_pics')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    picture_path = os.path.join(upload_folder, picture_f_name)
    form_picture.save(picture_path)
    
    return picture_f_name