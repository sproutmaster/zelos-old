from flask import Flask, render_template
from flask_oidc import OpenIDConnect
from admin.routes import admin
from print_status.routes import print_status
from api.user import api


app = Flask(__name__)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(print_status, url_prefix='/print-status')
app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
