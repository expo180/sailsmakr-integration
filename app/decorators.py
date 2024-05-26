from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(role_name):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def ceo_required(f):
    return role_required('CEO')(f)

def hr_manager_required(f):
    return role_required('HR Manager')(f)

def accountant_required(f):
    return role_required('Accountant')(f)

def project_manager_required(f):
    return role_required('Project Manager')(f)

def it_administrator_required(f):
    return role_required('IT Administrator')(f)

def team_leader_required(f):
    return role_required('Team Leader')(f)

def employee_required(f):
    return role_required('Employee')(f)

def sales_manager_required(f):
    return role_required('Sales Manager')(f)

def sales_or_project_manager_required(f):
    return role_required('Project Manager')(f) or role_required('Sales Manager')(f) 

def user_required(f):
    return role_required('User')(f)