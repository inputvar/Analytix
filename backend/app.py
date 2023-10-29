import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from flask_sqlalchemy import SQLAlchemy

app = Flask("flask analytix")
app.secret_key = "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"  # Update with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_database.db'  # Update with your database URI
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Allow HTTP traffic for local dev

db = SQLAlchemy(app)

# Create a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    user_type = db.Column(db.String(20))  # 'client', 'attorney', 'admin'

GOOGLE_CLIENT_ID = "9828613652-8t59jva6i7i7brt5uid15n7q96et41t1.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

def login_is_required(user_type):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if "google_id" not in session or (session["user_type"] != user_type):
                return abort(401)  # Authorization required
            else:
                return function()
        return wrapper
    return decorator

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    google_id = id_info.get("sub")
    name = id_info.get("name")
    user_type = determine_user_type(id_info.get("email"))  # Implement this function

    session["google_id"] = google_id
    session["name"] = name
    session["user_type"] = user_type

    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        user = User(google_id=google_id, name=name, user_type=user_type)
        db.session.add(user)
        db.session.commit()

    return redirect("/protected_area")

def determine_user_type(email):
    # Implement your logic here to determine the user type based on the email
    # For example, you can check the email domain or any other criteria
    # Return 'client', 'attorney', or 'admin' accordingly
    return "client"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"

@app.route("/protected_area")
@login_is_required("client")
def protected_area():
    return f"Hello {session['name']}! You are a {session['user_type']} user.<br/><a href='/logout'><button>Logout</button></a>"

@app.route("/attorney_dashboard")
@login_is_required("attorney")
def attorney_dashboard():
    return f"Hello {session['name']}! You are an {session['user_type']} user.<br/><a href='/logout'><button>Logout</button></a>"

@app.route("/admin_dashboard")
@login_is_required("admin")
def admin_dashboard():
    return f"Hello {session['name']}! You are an {session['user_type']} user.<br/><a href='/logout'><button>Logout</button></a>"

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
