import json
import requests
from app import appConf, oauth
from flask import Blueprint, abort, redirect, render_template, session, url_for

authentications = Blueprint('authentications', __name__, url_prefix='/auth', static_folder='static', template_folder= 'templates')

# list of google scopes - https://developers.google.com/identity/protocols/oauth2/scopes
oauth.register(
    "myApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read",
        # 'code_challenge_method': 'S256'  # enable PKCE
    },
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',
)

@authentications.route('/')
def home():
    return render_template("home.html", session=session.get("user"),
                           pretty=json.dumps(session.get("user"), indent=4))

@authentications.route("/login/callback")
def googleCallback():
    # fetch access token and id token using authorization code
    token = oauth.myApp.authorize_access_token()

    # google people API - https://developers.google.com/people/api/rest/v1/people/get
    # Google OAuth 2.0 playground - https://developers.google.com/oauthplayground
    # make sure you enable the Google People API in the Google Developers console under "Enabled APIs & services" section

    # fetch user data with access token
    personDataUrl = "https://people.googleapis.com/v1/people/me?personFields=genders,birthdays"
    personData = requests.get(personDataUrl, headers={
        "Authorization": f"Bearer {token['access_token']}"
    }).json()
    token["personData"] = personData
    # set complete user information in the session
    session["user"] = token
    return redirect(url_for("authentications.home"))


@authentications.route("/google-login")
def googleLogin():
    if "user" in session:
        abort(404)
    print(url_for("authentications.googleCallback", _external=True))
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("authentications.googleCallback", _external=True))


@authentications.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("authentications.home"))

