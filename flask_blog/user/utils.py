import os
import secrets
from PIL import Image
from flask import url_for, redirect,render_template,flash
from flask_blog import app
from flask_blog import db, bcrypt
from flask_blog.models import User

#  a function to update the profile picture;
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # this os.path.splitext(form_picture.filename) gives 2 value file name without extention
    #  and extention of the file name.
    _, f_ext = os.path.splitext(form_picture.filename)
    # we created a new name for the updated file
    picture_fn = random_hex + f_ext
    #  os.path.join   will simply copy the image from user device and will save it into our pics folder;
    picture_path = os.path.join(app.root_path, "static/pics", picture_fn)
    # resizing the picture to 125 pixel to save size of the filesystem
    #    wwe used Pillow lib from the Python to resize the image;
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn




