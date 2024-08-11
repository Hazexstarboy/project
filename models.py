from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), unique = True, nullable = False)
    password_hash = db.Column(db.String(140), nullable = False)
    role = db.Column(db.String(100), nullable = False)
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
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User", backref="sponsors")

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    niche = db.Column(db.String(100), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User", backref="influencers")

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(100), nullable=False)
    goals = db.Column(db.String(200), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("sponsor.id"))

    sponsor = db.relationship("Sponsor", backref="campaigns")

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencer.id"))
    messages = db.Column(db.String(200), nullable=False)
    requirements = db.Column(db.String(200), nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()
