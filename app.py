from flask import Flask, render_template, g, redirect, url_for, session
from flask_oidc import OpenIDConnect
from oauth2client.client import OAuth2Credentials
from okta.client import Client as OktaClient
from os import environ

from admin.routes import admin
from print_status.routes import print_status
from api.user import api

app = Flask(__name__)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(print_status, url_prefix='/print-status')
app.register_blueprint(api, url_prefix='/api')

app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = True
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
oidc = OpenIDConnect(app)

client_config = {
    "orgUrl": environ.get("OKTA_ORG_URL"),
    "token": environ.get("OKTA_TOKEN"),
}
okta_client = OktaClient(client_config)


@app.before_request
async def before_request():
    if oidc.user_loggedin:
        user_id = oidc.user_getfield("sub")
        g.user_id = user_id
        g.user, resp, err = await okta_client.get_user(user_id)
        session['access_token'] = OAuth2Credentials.from_json(oidc.credentials_store[g.user_id]).access_token
    else:
        g.user = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/dashboard")
@oidc.require_login
def dashboard():
    return render_template("dashboard.html")


@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".dashboard"))


@app.route("/logout")
async def logout():
    oidc.logout()
    session.clear()
    return render_template("logout.html", okta_url=environ.get("OKTA_ORG_URL"), redirect_url=url_for('index'))


if __name__ == '__main__':
    app.run()
