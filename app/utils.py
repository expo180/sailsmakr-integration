def get_tasks_for_user(user_email):
    from .models import Task
    tasks = Task.query.filter_by(assigned_to=user_email).all()

    return tasks
