from datetime import datetime, timedelta
from sqlalchemy import func, extract
from ..models import db, Authorization, Purchase, User, Role

def truncate_description(description, word_limit):
    words = description.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return description

def get_weekly_service_fees():
    today = datetime.utcnow()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    current_week_fees = db.session.query(
        func.sum(Authorization.service_fees + Purchase.service_fees)
    ).filter(
        (Authorization.date >= start_of_week) & (Authorization.date < end_of_week) |
        (Purchase.start_check >= start_of_week) & (Purchase.start_check < end_of_week)
    ).scalar()

    previous_week_start = start_of_week - timedelta(days=7)
    previous_week_end = start_of_week

    previous_week_fees = db.session.query(
        func.sum(Authorization.service_fees + Purchase.service_fees)
    ).filter(
        (Authorization.date >= previous_week_start) & (Authorization.date < previous_week_end) |
        (Purchase.start_check >= previous_week_start) & (Purchase.start_check < previous_week_end)
    ).scalar()

    return current_week_fees or 0, previous_week_fees or 0

def calculate_percentage_difference(current, previous):
    if previous == 0:
        return 100 if current > 0 else 0
    return ((current - previous) / previous) * 100

def get_weekly_financial_summary():
    current_week_fees, previous_week_fees = get_weekly_service_fees()
    percentage_difference = calculate_percentage_difference(current_week_fees, previous_week_fees)

    return {
        'current_week_fees': current_week_fees,
        'previous_week_fees': previous_week_fees,
        'percentage_difference': percentage_difference,
        'status': 'gain' if percentage_difference > 0 else 'loss'
    }


def get_user_role_count():
    user_role = Role.query.filter_by(name='User').first()
    if not user_role:
        return 0, 0 

    today = datetime.utcnow()
    start_of_current_month = datetime(today.year, today.month, 1)
    start_of_previous_month = (start_of_current_month - timedelta(days=1)).replace(day=1)
    end_of_previous_month = start_of_current_month - timedelta(days=1)

    current_month_count = db.session.query(func.count(User.id)).filter(
        User.role_id == user_role.id,
        User.member_since >= start_of_current_month
    ).scalar()

    previous_month_count = db.session.query(func.count(User.id)).filter(
        User.role_id == user_role.id,
        User.member_since >= start_of_previous_month,
        User.member_since < start_of_current_month
    ).scalar()

    return current_month_count, previous_month_count

def calculate_percentage_difference(current, previous):
    if previous == 0:
        return 100 if current > 0 else 0
    return ((current - previous) / previous) * 100

def get_monthly_user_summary():
    current_count, previous_count = get_user_role_count()
    percentage_difference = calculate_percentage_difference(current_count, previous_count)

    return {
        'current_count': current_count,
        'previous_count': previous_count,
        'percentage_difference': percentage_difference,
        'status': 'gain' if percentage_difference > 0 else 'loss'
    }

def get_daily_client_count():
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    today_authorizations = db.session.query(func.count(Authorization.id)).filter(
        func.date(Authorization.date) == today
    ).scalar()

    today_purchases = db.session.query(func.count(Purchase.id)).filter(
        func.date(Purchase.start_check) == today
    ).scalar()

    yesterday_authorizations = db.session.query(func.count(Authorization.id)).filter(
        func.date(Authorization.date) == yesterday
    ).scalar()

    yesterday_purchases = db.session.query(func.count(Purchase.id)).filter(
        func.date(Purchase.start_check) == yesterday
    ).scalar()

    today_clients = today_authorizations + today_purchases
    yesterday_clients = yesterday_authorizations + yesterday_purchases

    return today_clients, yesterday_clients

def calculate_percentage_difference(current, previous):
    if previous == 0:
        return 100 if current > 0 else 0
    return ((current - previous) / previous) * 100

def get_daily_client_summary():
    today_clients, yesterday_clients = get_daily_client_count()
    percentage_difference = calculate_percentage_difference(today_clients, yesterday_clients)

    return {
        'today_clients': today_clients,
        'yesterday_clients': yesterday_clients,
        'percentage_difference': percentage_difference,
        'status': 'gain' if percentage_difference > 0 else 'loss'
    }
