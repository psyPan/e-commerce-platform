from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash
from store import db, bcrypt

login = Blueprint('login', __name__)

@login.route('/')
@login.route('/home')
def home():
    return "Hello world"