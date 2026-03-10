from flask import Flask, render_template
from forms import RegisterForm, LoginForm

# Initialize flask app
app = Flask(__name__)

# Create a database

# Create a user model with id, email and password

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

