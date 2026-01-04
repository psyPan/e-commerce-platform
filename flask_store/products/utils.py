import os
from werkzeug.utils import secure_filename
from flask import current_app

def save_picture(form_picture):
    # Get secure filename
    filename = secure_filename(form_picture.filename)
    
    # Create directory if it doesn't exist
    upload_folder = os.path.join(current_app.root_path, 'static/product_pics')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # Handle duplicate filenames by adding numbers
    base_name, extension = os.path.splitext(filename)
    counter = 1
    picture_path = os.path.join(upload_folder, filename)
    
    while os.path.exists(picture_path):
        filename = f"{base_name}_{counter}{extension}"
        picture_path = os.path.join(upload_folder, filename)
        counter += 1
    
    form_picture.save(picture_path)
    
    return filename