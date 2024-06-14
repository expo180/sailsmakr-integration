def get_tasks_for_user(user_email):
    from .models import Task, User

    user = User.query.filter_by(email=user_email).first()
    if user:
        tasks = Task.query.filter_by(assigned_to=user.id).all()
    else:
        tasks = []

    return tasks
