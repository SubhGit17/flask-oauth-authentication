from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
from models import db, User

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)
with app.app_context():
    db.create_all()

oauth = OAuth(app)

google = oauth.register(
    name='google' ,
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        'scope': 'openid email profile'
    }
)

facebook = oauth.register(
    name='facebook',
    client_id=os.getenv("FACEBOOK_CLIENT_ID"),
    client_secret=os.getenv("FACEBOOK_CLIENT_SECRET"),
    access_token_url='https://graph.facebook.com/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    api_base_url='https://graph.facebook.com/',
    client_kwargs={
        'scope': 'email'
    }
)

x = oauth.register(
    name='x',
    client_id=os.getenv("X_CLIENT_ID"),
    client_secret=os.getenv("X_CLIENT_SECRET"),
    access_token_url='https://api.twitter.com/2/oauth2/token',
    authorize_url='https://twitter.com/i/oauth2/authorize',
    api_base_url='https://api.twitter.com/2/',
    client_kwargs={
        'scope': 'tweet.read users.read offline.access'
    },
    code_challenge_method="S256"
)

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    
    return render_template("login.html")

@app.route("/login/google")
def login_google():
    redirect_uri = url_for("authorize_google", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/login/facebook")
def login_facebook():
    redirect_uri = url_for("authorize_facebook", _external=True)
    return facebook.authorize_redirect(redirect_uri)

@app.route("/login/x")
def login_x():
    redirect_uri = url_for("authorize_x", _external=True)
    return x.authorize_redirect(redirect_uri)

@app.route("/authorize/google")
def authorize_google():
    token = google.authorize_access_token()
    resp = google.get("https://www.googleapis.com/oauth2/v2/userinfo")
    user_info = resp.json()

    user = User.query.filter_by(email=user_info["email"]).first()

    if not user:
        user = User(
            name=user_info["name"],
            email=user_info["email"],
            provider="Google"
        )
        db.session.add(user)
        db.session.commit()
    
    session["user"] = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "provider": user.provider
    }

    return redirect(url_for("dashboard"))

@app.route("/authorize/facebook")
def authorize_facebook():
    token = facebook.authorize_access_token()
    resp = facebook.get("me?fields=id,name,email")
    user_info = resp.json()

    user = User.query.filter_by(email=user_info["email"]).first()

    if not user:
        user = User(
            name=user_info["name"],
            email=user_info["email"],
            provider="Facebook"
        )
        db.session.add(user)
        db.session.commit()
    
    session["user"] = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "provider": user.provider
    }

    return redirect(url_for("dashboard"))

@app.route("/authorize/x")
def authorize_x():
    token = x.authorize_access_token()
    resp = x.get("users/me")
    user_info = resp.json()

    user = User.query.filter_by(email=user_info["data"]["id"]).first()

    if not user:
        user = User(
            name=user_info["data"]["name"],
            email=f"{user_info['data']['id']}@x.com",
            provider="X"
        )
        db.session.add(user)
        db.session.commit()
    
    session["user"] = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "provider": user.provider
    }

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))
    
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/delete")
def delete_data():
    return "To delete your data, contact: shubhusourav17@gmail.com"

if __name__ == "__main__":
    app.run()