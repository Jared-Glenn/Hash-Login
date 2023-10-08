"""User and Feedback models detailed."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to the database."""
    db.app = app
    db.init_app(app)
    

class User(db.Model):
    """User model."""
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(20),
                         unique=True,
                         nullable=False)
    password = db.Column(db.String(),
                         nullable=False)
    email = db.Column(db.String(50),
                      unique=True,
                      nullable=False)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
        
    def __repr__(self):
        return f"<User {self.id} {self.username} {self.password} {self.email} {self.first_name} {self.last_name} >"
    
    
class Feedback(db.Model):
    """Feedback model."""
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.String(),
                        nullable=False)
    username = db.Column(db.String(20),
                         db.ForeignKey('users.username'),
                         nullable=False)
    
    def __repr__(self):
        return f"<Feedback {self.id} {self.title} {self.content} {self.username} >"

