from flask import Blueprint

api = Blueprint('api', __name__)


@api.route('/')
def send_api_info():
    return {
        'api': 'v1',
        'last_updated': '00:00:00'
    }
