from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), unique = True, nullable = False)
    password_hash = db.Column(db.String(140), nullable = False)
    name = db.Column(db.String(32), nullable = False)
    is_admin = db.Column(db.Boolean, nullable = False, default = False)

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Sponsor(db.Model):
    __tablename__ = 'sponser'
    id = db.Column(db.Integer, primary_key=True)
    industry = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User", backref="sponsors")

class Influencer(db.Model):
    __tablename__ = 'influencer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    platform = db.Column(db.String(100), nullable=False)

    user = db.relationship("User", backref="influencers")

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(username = 'admin').first()
    if not admin:
        admin = User(username = 'admin',name = 'admin', password = 'admin', is_admin = True)
        db.session.add(admin)
        db.session.commit()
