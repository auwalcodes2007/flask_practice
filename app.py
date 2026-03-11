from flask import Flask, render_template, redirect, url_for, flash
from models import db, User
from sqlalchemy.exc import IntegrityError
from forms import RegisterForm, LoginForm
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

load_dotenv()

# Initialize login manager
login_manager = LoginManager()

# Initialize flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
db.init_app(app)
login_manager.init_app(app)

# Create the User Loader
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


# Create tables
with app.app_context():
    db.create_all()

# Create home route
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

# Create register route
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Get form data and hash password
        hashed_password = generate_password_hash(form.password.data, salt_length=16)
        user = User(email=form.email.data, password=hashed_password)
        # Add user to database using try/except
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('dashboard'))
        except IntegrityError:
            flash("Email already exists")
            return redirect(url_for('login'))

    if form.errors:
        print(f"Form error: {form.errors}")
        
    return render_template("register.html", form=form)

# Create login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Sorry, invalid credentials")
    return render_template("login.html", form=form)

# Create Dashboard route
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# Create Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# Error handler to redirect unauthorized access
@app.errorhandler(401)
def unauthorized(e):
    return render_template("denied.html"), 401