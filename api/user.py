from api import api


@api.route('/user/add', methods=['POST'])
def add():
    return 'Hello user!'

