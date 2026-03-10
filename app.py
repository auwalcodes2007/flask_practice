from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from forms import RegisterForm, LoginForm

# Initialize flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create a database
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Create a user model with id, email and password

# Create tables

# Create home route
@app.route("/")
def home():
    return render_template("index.html")

# Create register route
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)

# Create login route
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

