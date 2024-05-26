from flask import request, render_template, session, jsonify, url_for, redirect, flash, abort
from flask_babel import _
from . import main
from ..models import User, Task, Role, Event, Invoice, ClientInvoice, Note, Job, Employee, JobApplication, MarketingCampaign, Purchase, Authorization
from flask_login import current_user, login_required, login_user
from ..decorators import ceo_required, hr_manager_required, project_manager_required, employee_required, sales_manager_required, user_required, accountant_required
from .. import db
import os
from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
from ._utils import truncate_description
from datetime import datetime

load_dotenv()


@main.route("/")
def home():
    return render_template("main/home.html")

@main.route("/cgu")
def cgu():
    return render_template("main/cgu.html")

@main.route("/home")
@login_required
def user_home():
    return render_template(
        "dashboard/user_home.html"
    )

@main.route("/careers/job_list")
@login_required
@hr_manager_required
def job_list():
    jobs = Job.query.all()
    return render_template('api/@support_team/jobs/job_list.html', jobs=jobs)

@main.route("/settings")
@login_required
def settings():
    return render_template("dashboard/settings.html")

@main.route("/calendar")
@login_required
@employee_required
def calendar():
    return render_template("dashboard/@support_team/calendar.html")

@main.route("/calculator")
@login_required
def calculator():
    return render_template("dashboard/calculator.html")

@main.route("/my_purchases/previous_purchase_requests")
@login_required
@user_required
def previous_purchase_requests():
    purchases = Purchase.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard/customers/previous_purchase_requests.html", purchases=purchases)

@main.route("/purchases/<int:id>", methods=['GET'])
@login_required
@user_required
def get_purchase_details(id):
    purchase = Purchase.query.get_or_404(id)
    if purchase.user_id != current_user.id:
        abort(403)
    return jsonify({
        'title': purchase.title,
        'token': purchase.token,
        'status': purchase.status,
        'start_check': purchase.start_check,
        'description': purchase.description,
        'author_first_name': purchase.author_first_name,
        'author_last_name': purchase.author_last_name,
        'author_email_address': purchase.author_email_address,
        'author_phone_number': purchase.author_phone_number,
        'author_address': purchase.author_address,
        'author_country': purchase.location,
        'qr_code_url': purchase.qr_code_url
    })


@main.route("/quotes/previouses")
@login_required
@user_required
def previous_quotes():
    user_id = current_user.id
    user_requests = Authorization.query.filter_by(user_id=user_id).all()
    return render_template("dashboard/customers/previous_quotes.html", user_requests=user_requests)

@main.route("/mailbox/sent_messages")
@login_required
def sent_messages():
    return render_template("dashboard/sent_messages.html")

@main.route("/notes/previous_notes")
@login_required
@ceo_required
def previous_notes():
    previous_notes = Note.query.all()
    return render_template(
        "dashboard/@support_team/previous_notes.html",
        previous_notes=previous_notes
    )

@main.route("/careers/new_jobs")
@login_required
def new_jobs():
    return render_template("dashboard/jobs_listing.html")

@main.route("/careers/previous_created_jobs")
@login_required
@hr_manager_required
def previous_created_jobs():
    jobs = Job.query.all()
    return render_template(
        "dashboard/@support_team/previous_created_jobs.html",
        jobs=jobs
    )

@main.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    if request.method == 'POST':
        title = request.form.get('title')
        status = request.form.get('status')
        description = request.form.get('description')
        assigned_to = request.form.get('assigned_to')

        new_task = Task(title=title, status=status, description=description, assigned_to=assigned_to)
        db.session.add(new_task)
        db.session.commit()

        return jsonify({'success': True})

    tasks = Task.query.all()
    users = User.query.join(Role).filter(Role.name.in_([
        'Employee', 'HR Manager', 'Accountant', 'Project Manager', 'IT Administrator', 'Team Leader'
    ])).all()

    return render_template("dashboard/@support_team/tasks.html", users=users, tasks=tasks)


@main.route("/events", methods=['GET', 'POST'])
@login_required
@ceo_required
def events():
    return render_template("dashboard/@support_team/events.html")

@main.route("/get_events", methods=['GET'])
@login_required
def get_events():
    events = Event.query.all()
    events_list = []
    for event in events:
        events_list.append({
            'title': event.title,
            'start': event.start_from.isoformat(),
            'end': event.end_at.isoformat(),
        })
    return jsonify(events_list)

@main.route("/ads", methods=["GET", "POST"])
@login_required
def ads():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        objectives = request.form.get("objectives")
        start_from = request.form.get("start_from")
        end_at = request.form.get("end_at")
        min_budget = request.form.get("min_budget")
        max_budget = request.form.get("max_budget")
        start_from_dt = datetime.fromisoformat(start_from)
        end_at_dt = datetime.fromisoformat(end_at)

        new_ad = MarketingCampaign(
            title=title,
            description=description,
            objectives=objectives,
            start_from=start_from_dt,
            end_at=end_at_dt,
            min_budget=min_budget,
            max_budget=max_budget
        )

        db.session.add(new_ad)
        db.session.commit()

        return jsonify({'success' : True, 'message' :  _('Votre nouvelle campagne a été ajoutée, vous pouvez maintenant tirer le meilleur de votre audience') })

    ads = MarketingCampaign.query.all()
    return render_template("dashboard/@support_team/ads.html", ads=ads)

@main.route("/reports/finances")
@login_required
@ceo_required
def report_finances():
    return render_template("dashboard/@support_team/finance_reports.html")

@main.route("/reports/marketplace_data")
@login_required
@ceo_required
def marketplace_data():
    return render_template("dashboard/@support_team/marketplace.html")

@main.route("/new_purchases")
@login_required
@sales_manager_required
def new_purchases():
    purchases = Purchase.query.filter_by(status=False).all()
    return render_template("dashboard/@support_team/new_purchases.html", purchases=purchases)

@main.route("/messages/inbox")
@login_required
def inbox():
    return render_template("dashboard/new_messages.html")

@main.route("/invoices", methods=['GET', 'POST'])
@login_required
@accountant_required
def invoices():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        amount = data.get('amount')
        description = data.get('description', '')

        if not title or not amount:
            return jsonify({'message': 'Title and amount are required!'}), 400

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return jsonify({'message': 'Invalid amount!'}), 400

        new_invoice = Invoice(title=title, amount=amount, description=description)
        db.session.add(new_invoice)
        db.session.commit()
        return jsonify({'message': 'Invoice created successfully!'}), 201

    invoices = Invoice.query.all()
    return render_template("dashboard/@support_team/invoices.html", invoices=invoices)

@main.route("/careers/recent_applications", methods=['GET'])
@login_required
@hr_manager_required
def recent_applications():
    jobs = Job.query.all()
    selected_job_id = request.args.get('job_id')
    applications = []

    if selected_job_id:
        selected_job = Job.query.get_or_404(selected_job_id)
        if selected_job:
            applications = JobApplication.query.filter_by(job_id=selected_job_id).order_by(JobApplication.apply_at.desc()).all()

    return render_template('dashboard/@support_team/applicants_list.html', jobs=jobs, applications=applications, selected_job_id=selected_job_id)

@main.route("/careers/employees_table")
@login_required
@hr_manager_required
def employee_table():
    employees = Employee.query.all()
    return render_template(
        'dashboard/@support_team/employees_listing.html',
        employees=employees
    )

@main.route("/my_invoices")
@login_required
def client_invoices():
    return render_template("dashboard/@support_team/client_inoices.html")

@main.route("/my_purchases/track_my_product")
@user_required
@login_required
def live_tracking():
    return render_template('dashboard/customers/live_tracking.html')


@main.route("/careers/my_recent_applications")
@login_required
def my_recent_applications(user_id):
    return render_template("dashboard/customers/my_recent_applications.html")