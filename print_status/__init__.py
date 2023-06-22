from flask import Blueprint, render_template

print_status = Blueprint('print_status', __name__, static_folder='static', template_folder='templates')
