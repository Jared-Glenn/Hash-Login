"""Routes for each page."""

from flask import Flask, request, render_template, redirect, jsonify, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hash-login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()

bcrypt = Bcrypt()


# Main page

@app.route('/')
def home():
    """User homepage. Redirects to Register."""
    
    return redirect('/register')


# Registration page

@app.route('/register', methods=["GET", "POST"])
def register():
    """Register a new user."""
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        hashed = bcrypt.generate_password_hash(form.password.data)
        password = hashed.decode("utf8")
        
        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        
        session["username"] = new_user.username
        
        return redirect(f'/users/{new_user.username}')
    else:
        return render_template("register.html", form=form)

# Login page

@app.route('/login', methods=["GET", "POST"])
def login():
    """Login to site."""
    
    form =LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            
            session["username"] = user.username
            
            return redirect(f'/users/{username}')
        
        else:
            form.username.errors = ["Invalid username or password."]
            
    return render_template("login.html", form=form)


# Secret page for user information.

@app.route('/users/<username>', methods=["GET"])
def user_info(username):
    """Secret page for user information."""
    
    if "username" not in session:
        flash("Please log in first!")
        
        return redirect('/login')
    
    if username != session["username"]:
        flash("You can only access your own user page.")
        
        return redirect('/login')
    
    user = User.query.filter_by(username=username).first()
    
    feedback = Feedback.query.filter_by(username=username).all()
    
    return render_template("user.html", user=user, feedback=feedback)


# Logout

@app.route('/logout', methods=["GET"])
def logout():
    """Route for logging a user out."""
    
    session.pop("username")
    
    return redirect('/')


# Delete user

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Delete a user. Only available while logged in as that user."""
    
    if "username" not in session:
        flash("Please log in first!")
        
        return redirect('/login')
    
    if username != session["username"]:
        flash("You can only delete a user while logged in as that user.")
        
        return redirect('/login')
    
    
    user = User.query.filter_by(username=username).first()
    
    db.session.delete(user)
    db.session.commit()
    
    session.pop("username")
    
    return redirect('/')


# Feedback Add Form

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def provide_feedback(username):
    """Provide new feedback."""
    
    form = FeedbackForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        new_feedback = Feedback(title=title, content=content, username=username)
        
        db.session.add(new_feedback)
        db.session.commit()
        
        return redirect(f'/users/{username}')
            
    return render_template("new_feedback.html", form=form)


# Update Feedback

@app.route('/feedback/<feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Update feedback."""
    
    feedback = Feedback.query.get_or_404(feedback_id)
    
    form = FeedbackForm(obj=feedback)
    
    if form.validate_on_submit():
        
        if "username" not in session:
            flash("Please log in first!")

            return redirect('/login')
    
        if feedback.username != session["username"]:
            flash("You can only update your own feedback.")

            return redirect('/login')
        
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()
        
        return redirect(f'/users/{feedback.username}')
    
    return render_template("edit_feedback.html", form=form)


# Delete Feedback

@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""
    
    feedback = Feedback.query.get_or_404(feedback_id)
    
    if "username" not in session:
        flash("Please log in first!")
        
        return redirect('/login')
    
    if feedback.username != session["username"]:
        flash("You can only delete your own feedback.")
        
        return redirect('/login')
    
    db.session.delete(feedback)
    db.session.commit()
    
    return redirect(f'/users/{feedback.username}')