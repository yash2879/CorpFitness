from flask import Flask, render_template
from authlib.integrations.flask_client import OAuth
app = Flask(__name__)
app.config['DEBUG']=True

appConf = {
    "OAUTH2_CLIENT_ID": "736795970057-29rk340p17987v0q2ctle8n5f73lloak.apps.googleusercontent.com",
    "OAUTH2_CLIENT_SECRET": "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",
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": "hELLO",
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")
oauth = OAuth(app)
from auth.authentications import authentications
app.register_blueprint(authentications)