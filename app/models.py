# app/models.py
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import Serializer
from . import db
from . import login_manager
from dotenv import load_dotenv
import os

load_dotenv()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    description = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    @staticmethod
    def insert_roles():
        roles = {
            'CEO': 'Oversee all company operations and strategy',
            'HR Manager': 'Manage human resources tasks and employee relations',
            'Accountant': 'Handle financial tasks, bookkeeping, and transactions',
            'Project Manager': 'Oversee project planning, execution, and completion',
            'Sales Manager': 'Manage sales activities, analyse marketing data',
            'IT Administrator': 'Manage and support IT infrastructure and systems',
            'Team Leader': 'Lead and coordinate tasks within a specific team',
            'Employee': 'Perform tasks and duties assigned in their specific role',
            'User': 'A generic user role'
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.description = roles[r]
            role.default = (r == 'User')
            db.session.add(role)
        db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(128))
    password_hash = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(64))
    name = db.Column(db.String(64))
    gender = db.Column(db.String())
    address = db.Column(db.String())
    profile_picture_url = db.Column(db.String)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    authorizations = db.relationship('Authorization', backref='user', lazy='dynamic')
    purchases = db.relationship('Purchase', back_populates='user', lazy=True)
    tasks = db.relationship('Task', lazy=True)
    invoices = db.relationship('ClientInvoice', lazy=True)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def get_authorization_client_phone_number(self):
        authorization = Authorization.query.filter_by(user_id=self.id).first()
        if authorization:
            return authorization.client_phone_number
        return None

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        
        if data.get('confirm') != self.id:
            return False
        
        self.confirmed = True
        db.session.add(self)
        return True

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        
        agents_emails = os.getenv("AGENTS_EMAILS")
        AGENTS_EMAILS = agents_emails.split(',')

        if self.email == current_app.config['COMPANY_CEO']:
            self.role = Role.query.filter_by(name='CEO').first()

        if self.email == current_app.config['COMPANY_CEO_ASSISTANT']:
            self.role = Role.query.filter_by(name='CEO').first()

        elif self.email == current_app.config['COMPANY_HR_MANAGER']:
            self.role = Role.query.filter_by(name='HR Manager').first()

        elif self.email == current_app.config['COMPANY_ACCOUNTANT']:
            self.role = Role.query.filter_by(name='Accountant').first()

        elif self.email == current_app.config['COMPANY_PROJECT_MANAGER']:
            self.role = Role.query.filter_by(name='Project Manager').first()

        elif self.email == current_app.config['COMPANY_SALES_MANAGER']:
            self.role = Role.query.filter_by(name='Sales Manager').first()

        elif self.email == current_app.config['COMPANY_IT_ADMINISTRATOR']:
            self.role = Role.query.filter_by(name='IT Administrator').first()

        elif self.email in AGENTS_EMAILS:
            self.role = Role.query.filter_by(name='Employee').first()

        else:
            self.role = Role.query.filter_by(default=True).first()

    @property
    def role_names(self):
        return [self.role.name]

    def has_role(self, role_name):
        return self.role.name == role_name




class Authorization(db.Model):
    __tablename__ = 'authorizations'
    id = db.Column(db.Integer, primary_key=True)
    client_first_name = db.Column(db.String, nullable=False, unique=True)
    client_first_name = db.Column(db.String, nullable=False, unique=True)
    client_phone_number = db.Column(db.String, nullable=False, unique=True)
    client_email_adress = db.Column(db.String, unique=True)
    client_id_card_url = db.Column(db.String)
    client_signature_url = db.Column(db.String)
    agent_first_name = db.Column(db.String, nullable=False)
    agent_last_name = db.Column(db.String, nullable=False)
    agent_email_adress = db.Column(db.String)
    shipping_company_title = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    client_signature_url = db.Column(db.String, nullable=False)
    provider_email1 = db.Column(db.String, nullable=False)
    provider_email2 = db.Column(db.String)
    provider_email3 = db.Column(db.String)
    provider_email4 = db.Column(db.String)
    provider_name1 = db.Column(db.String, nullable=False)
    provider_name2 = db.Column(db.String)
    provider_name3 = db.Column(db.String)
    provider_name4 = db.Column(db.String)
    lading_bills_identifier = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Article(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref='posts')

class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    id = db.Column(db.Integer, primary_key=True)
    applicant_first_name = db.Column(db.String, nullable=False)
    applicant_last_name = db.Column(db.String, nullable=False)
    applicant_email_address = db.Column(db.String, nullable=False)
    applicant_location = db.Column(db.String, nullable=False)
    motivation = db.Column(db.Text, nullable=False)
    linkedin_url = db.Column(db.String)
    github_url = db.Column(db.String)
    dribble_url = db.Column(db.String)
    date_of_birth = db.Column(db.DateTime())
    apply_at = db.Column(db.DateTime(), default=datetime.utcnow)
    CV_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='job_applications')
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float)
    posted_date = db.Column(db.DateTime, nullable=False)
    closing_date = db.Column(db.DateTime)
    applications = db.relationship('JobApplication', backref='job', lazy=True)

class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Float, default=0.0)
    qr_code_url = db.Column(db.String())
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

class ClientInvoice(db.Model):
    __tablename__ = 'client_invoices'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Float, default=0.0)
    qr_code_url = db.Column(db.String())
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class MarketingCampaign(db.Model):
    __tablename__ = 'marketing_campaigns'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    objectives = db.Column(db.Text, nullable=False)
    start_from = db.Column(db.DateTime(), default=datetime.utcnow)
    end_at = db.Column(db.DateTime(), default=datetime.utcnow)
    min_budget = db.Column(db.Float, default=0.0)
    max_budget = db.Column(db.Float, default=0.0)
    debt = db.Column(db.Float, default=0.0)

class MarketingCampaignTool(db.Model):
    __tablename__ = 'marketing_campaign_tools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    cost = db.Column(db.Float)

marketing_campaign_tool_association = db.Table('marketing_campaign_tool_association', db.Model.metadata,
    db.Column('marketing_campaign_id', db.Integer, db.ForeignKey('marketing_campaigns.id')),
    db.Column('marketing_campaign_tool_id', db.Integer, db.ForeignKey('marketing_campaign_tools.id'))
)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    objectives = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    objectives = db.Column(db.Text, nullable=False)
    start_from = db.Column(db.DateTime(), default=datetime.utcnow)
    end_at = db.Column(db.DateTime(), default=datetime.utcnow)
    min_budget = db.Column(db.Float, default=0.0)
    max_budget = db.Column(db.Float, default=0.0)
    debt = db.Column(db.Float, default=0.0)
    status = db.Column(db.Float, default=False)


    
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    employee_first_name = db.Column(db.String)
    employee_last_name = db.Column(db.String)
    employee_email_address = db.Column(db.String, nullable=False)
    employee_services = db.Column(db.String)
    employee_job_title = db.Column(db.String, nullable=False)
    employee_wage = db.Column(db.Float, default=0.0)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    employee_date_of_birth = db.Column(db.DateTime())
    picture_url = db.Column(db.String)
    qr_code_url = db.Column(db.String)
    professional_card_url = db.Column(db.String)
    identifier = db.Column(db.String(), nullable=False)
    


class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=False)
    author_first_name = db.Column(db.String, nullable=False)
    author_last_name = db.Column(db.String, nullable=False)
    author_email_address = db.Column(db.String, nullable=False)
    product_length = db.Column(db.Float, default=0.0)
    product_width = db.Column(db.Float, defautlt=0.0)
    author_phone_number = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    provider = db.Column(db.String)
    product_picture_url = db.Column(db.String)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, default=False)
    name = db.Column(db.String())
    category = db.Column(db.String)
    doc_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='purchases')
    start_check = db.Column(db.DateTime(), default=datetime.utcnow)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(128))
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    status = db.Column(db.String)
    start_from = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    report = db.Column(db.Text)


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    nature = db.Column(db.String)

