from functools import wraps
from flask import abort, current_app
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

def user_required(f):
    return role_required('User')(f)

def has_role(role_name):
    return current_user.is_authenticated and current_user.has_role(role_name)

def is_ceo():
    return has_role('CEO')

def is_hr_manager():
    return has_role('HR Manager')

def is_accountant():
    return has_role('Accountant')

def is_project_manager():
    return has_role('Project Manager')

def is_it_administrator():
    return has_role('IT Administrator')

def is_team_leader():
    return has_role('Team Leader')

def is_employee():
    return has_role('Employee')

def is_sales():
    return has_role('Sales Manager')

def is_user():
    return has_role('User')

def inject_role_helpers(app):
    app.context_processor(lambda: {
        'is_ceo': is_ceo,
        'is_hr_manager': is_hr_manager,
        'is_accountant': is_accountant,
        'is_project_manager': is_project_manager,
        'is_it_administrator': is_it_administrator,
        'is_team_leader': is_team_leader,
        'is_employee': is_employee,
        'is_sales': is_sales,
        'is_user': is_user,
        'has_role': has_role,
    })
