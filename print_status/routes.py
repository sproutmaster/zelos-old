from print_status import print_status
from flask import render_template, Flask


@print_status.route('/')
def hello_world():
    return 'Hello print!'
