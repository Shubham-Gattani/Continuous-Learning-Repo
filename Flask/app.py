from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy




# First create the db object using the SQLAlchemy constructor.
from db_object import db # Once constructed, the db object gives you access to the db.Model class to define models, and the db.session to execute queries.
from models import User

# create the app
app = Flask(__name__)

# next step is to connect the extension to your Flask app. The only required Flask app config is the SQLALCHEMY_DATABASE_URI key. That is a connection string that tells SQLAlchemy what database to connect to.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning

# initialize the app with the extension
db.init_app(app)


@app.route("/")
def home():
    # get all users
    all_users = User.query.all()
    return render_template("index.html", all_users=all_users)

@app.route("/add_new_user", methods=["POST"])
def add_new_user():
    name = request.form.get("user_name", "no_name_provided")
    age = int(request.form.get("user_age", 0))
    user = User(name=name, age=age)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

@app.route("/update_user_form/<int:user_id>", methods = ["GET", "POST"])
def update_user_form(user_id):
    if request.method=="POST":
        name = request.form.get("user_name", "no_name_provided")
        age = int(request.form.get("user_age", 0))
        user = User.query.get(user_id)
        user.name = name
        user.age=age
        db.session.commit()
        return redirect("/")
    else:
        user = User.query.get(user_id)
        return render_template("update_user_form.html", user=user)




if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)