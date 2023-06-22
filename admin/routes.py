from admin import admin
from flask import render_template, Flask


@admin.route('/')
def hello_world():
    return 'Hello Admin!'
