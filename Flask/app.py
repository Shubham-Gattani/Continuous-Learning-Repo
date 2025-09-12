from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore # SQLAlchemyUserDatastore is a helper that knows how to create users/roles in the DB. Security(app, datastore) sets up login, register, role checks, etc.
from flask_migrate import Migrate
from flask_security import roles_required, auth_required

from models import User, Role
# First create the db object using the SQLAlchemy constructor.
from db_object import db # Once constructed, the db object gives you access to the db.Model class to define models, and the db.session to execute queries.

# create the app
app = Flask(__name__)

# Configure App for Security BEFORE creating security instance
app.config["SECRET_KEY"] = "some_secret_key"
app.config["WTF_CSRF_ENABLED"] = False  # This disables CSRF completely
app.config["SECURITY_TOKEN_AUTHENTICATION_HEADER"] = "Authentication-Token"
app.config["SECURITY_PASSWORD_SALT"] = "some_random_salt"   # used for password hashing tokens
app.config["SECURITY_PASSWORD_HASH"] = "bcrypt"             # modern strong hash
app.config["SECURITY_REGISTERABLE"] = True                  # allow self-registration; meaning users can register themselves on their own without admin
app.config["SECURITY_SEND_REGISTER_EMAIL"] = False          # disable email (keep simple)
app.config["SECURITY_USERNAME_ENABLE"] = True               # enable login with username
app.config["SECURITY_LOGIN_WITHOUT_CONFIRMATION"] = True
app.config["SECURITY_USER_IDENTITY_ATTRIBUTES"] = [{"username": {"mapper": None, "case_insensitive": True}}]

# Additional configs to fix login form
app.config["SECURITY_LOGIN_USER_TEMPLATE"] = "security/login_user.html"  # Optional: use custom template
app.config["SECURITY_TRACKABLE"] = False  # Disable user tracking features
app.config["SECURITY_CHANGEABLE"] = True  # Allow password changes
app.config["SECURITY_RECOVERABLE"] = False  # Disable password recovery (no email)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning

# Initialize extensions
db.init_app(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
migrate = Migrate(app, db)

"""
At this point:
The app has /login, /logout, /register routes automatically.
Users can self-register (username/password).
Passwords are hashed.
CSRF is disabled to avoid token issues.
Username field should appear on login form.
"""

@app.route("/")
@auth_required()
def home():
    # get all users
    all_users = User.query.all()
    return render_template("index.html", all_users=all_users)

@app.route("/add_new_user", methods=["POST"])
@auth_required()
def add_new_user():
    name = request.form.get("user_name", "no_name_provided")
    age = int(request.form.get("user_age", 0))
    user = User(username=name, age=age)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete_user/<int:user_id>")
@auth_required()
@roles_required("admin")
def delete_user(user_id):
    user = db.session.get(User,user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

@app.route("/update_user_form/<int:user_id>", methods = ["GET", "POST"])
@auth_required()
@roles_required("user")
def update_user_form(user_id):
    if request.method=="POST":
        name = request.form.get("user_name", "no_name_provided")
        age = int(request.form.get("user_age", 0))
        user = db.session.get(User, user_id)
        user.username = name
        user.age=age
        db.session.commit()
        return redirect("/")
    else:
        user = User.query.get(user_id)
        return render_template("update_user_form.html", user=user)

@app.errorhandler(403)
def forbidden(error):
    # return render_template('403.html'), 403
    """
    Create templates/403.html:
    <h1>Access Denied</h1>
    <p>You don't have permission to access this resource.</p>
    <p>Required role: user</p>
    <a href="{{ url_for('home') }}">Go Home</a>
    """
    return "<h2>Custom error! Roles required.<h2>", 403

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)