from flask import request, render_template, session, jsonify, url_for, redirect, flash, abort
from flask_babel import _
from . import main
from ..models import User, Task, Role, Event, Invoice, Note, Job, Employee, JobApplication, MarketingCampaign, Purchase, Authorization, Store, Product
from flask_login import current_user, login_required, login_user
from ..decorators import ceo_required, hr_manager_required, project_manager_required, employee_required, sales_manager_required, user_required, accountant_required, reseller_required
from .. import db
import os
from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
from ._utils import truncate_description, get_weekly_financial_summary, get_monthly_user_summary, get_daily_client_summary, get_user_invoices, generate_password
from datetime import datetime
from ..api.utils import save_files, save_product_pictures, generate_barcode
from .emails import send_reseller_email
from werkzeug.security import generate_password_hash
import barcode
from barcode.writer import ImageWriter


load_dotenv()


@main.route("/")
def home():
    return render_template(
        "main/home.html"
    )


@main.route("/cgu")
def cgu():
    return render_template("main/cgu.html")

@main.route("/services/transit&manutention")
def transit():
    return render_template("main/transit.html")

@main.route("/services/customs")
def customs():
    return render_template("main/customs.html")

@main.route("/services/warehousing")
def warehousing():
    return render_template("main/warehousing.html")

@main.route("/fret-services/aerien")
def aerien():
    return render_template("main/aerien.html")

@main.route("/fret-services/sea")
def sea():
    return render_template("main/sea.html")

@main.route("/fret-services/terrestre")
def terrestre():
    return render_template("main/terrestre.html")

@main.route("/fret-sevices/air/calculate")
def calculate_air_freight():
    return render_template("main/calculate_air_freight.html")

@main.route("/fret-sevices/sea/calculate")
def calculate_sea_freight():
    return render_template("main/calculate_sea_freight.html")

@main.route("/fret-sevices/sea/calculate")
def calculate_truck_freight():
    return render_template("main/calculate_truck_freight.html")

@main.route("/fret-sevices/see-glossary")
def glossary():
    return render_template("main/glossary.html")

@main.route("/job-opennings")
def jobs():
    job_openings = Job.query.all()
    return render_template(
        "main/job_opennings.html",
        job_openings=job_openings
    )


@main.route("/sailsmakr-services/shop")
def shop():
    products = Product.query.filter_by(publish=True).all()
    return render_template("main/shop.html", products=products)

@main.route("/home")
@login_required
def user_home():
    api = NewsDataApiClient(apikey=os.environ.get('NEWS_API_KEYS'))

    summary = get_weekly_financial_summary()
    user_summary = get_monthly_user_summary()
    client_summary = get_daily_client_summary()
    invoices = get_user_invoices(current_user.id)
    published_products = Product.query.filter_by(user_id=current_user.id).all()
    new_products = Product.query.all()
    purchases = Purchase.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "dashboard/user_home.html",
        summary=summary,
        user_summary=user_summary,
        client_summary=client_summary,
        invoices=invoices,
        purchases=purchases,
        published_products=published_products,
        new_products=new_products
    
    )

@main.route("/my-previous-applications", methods=['GET'])
@login_required
def my_previous_applications():
    user_applications = JobApplication.query.filter_by(user_id=current_user.id).all()
    return render_template(
        'dashboard/applied_jobs_listing.html', 
        user_applications=user_applications
    )


@main.route("/products", methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@reseller_required
def products():
    if request.method == 'POST':
        title = request.form.get('title')
        cost = float(request.form.get('cost'))
        stock = int(request.form.get('stock', 0))
        category = request.form.get('category')
        provider = request.form.get('provider')
        provider_location = request.form.get('provider_location')
        publish = 'publish' in request.form
        image_file = request.files.get('product_img_url')

        if not category:
            return jsonify({"success": False, "message": "Category is required"}), 400

        if image_file:
            image_urls = save_files([image_file], "shop_product_images")
            product_img_url = image_urls[0] if image_urls else None
        else:
            product_img_url = None

        new_product = Product(
            title=title,
            cost=cost,
            stock=stock,
            category=category,
            provider=provider,
            provider_location=provider_location,
            product_img_url=product_img_url,
            publish=publish,
            user_id=current_user.id
        )
        db.session.add(new_product)
        db.session.commit()

        barcode_url = generate_barcode(new_product.id)
        new_product.barcode_url = barcode_url
        db.session.commit()

        return redirect(url_for('main.products'))

    elif request.method == 'PUT':
        product_id = request.form.get('id')
        product = Product.query.get_or_404(product_id)

        title = request.form.get('title')
        cost = float(request.form.get('cost'))
        stock = int(request.form.get('stock', 0))
        category = request.form.get('category')
        publish = 'publish' in request.form
        product_img = request.files.get('product_img_url')


        if product_img:
            product_img_url = save_files([product_img], 'shop_product_images')[0]
        else:
            product_img_url = product.product_img_url

        product.title = title
        product.cost = cost
        product.stock = stock
        product.category = category
        product.product_img_url = product_img_url
        product.publish = publish

        db.session.commit()

        barcode_url = generate_barcode(product.id)
        product.barcode_url = barcode_url
        db.session.commit()

        return jsonify({"success": True}), 200

    elif request.method == 'DELETE':
        product_id = request.form.get('id')
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()

        return jsonify({"success": True}), 200

    else:
        products = Product.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard/@support_team/products.html', products=products)

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
def calendar():
    return render_template("dashboard/@support_team/calendar.html")

@main.route("/calculator")
@login_required
def calculator():
    return render_template("dashboard/calculator.html")

@main.route('/stores', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@sales_manager_required
def stores():
    if request.method == 'GET':
        stores = Store.query.all()
        return render_template('dashboard/@support_team/stores.html', stores=stores)

    elif request.method == 'POST':
        data = request.form
        logo_files = request.files.getlist('logo')
        logo_urls = save_files(logo_files, 'store_logos')
        logo_url = logo_urls[0] if logo_urls else None

        password = generate_password()
        hashed_password = generate_password_hash(password)

        new_user = User(
            email=data['email'],
            password_hash=hashed_password,
        )

        db.session.add(new_user)
        db.session.commit()

        stored_user = User.query.filter_by(email=data['email']).first()

        if stored_user:
            reseller_role = Role.query.filter_by(name='Reseller').first()
            stored_user.role_id = reseller_role.id
            db.session.commit() 

        store = Store(
            name=data['name'],
            location=data['location'],
            email=data['email'],
            phone=data.get('phone'),
            logo_file_url=logo_url
        )

        db.session.add(store)
        db.session.commit()

        send_reseller_email(new_user.email, password)

        return jsonify(message="Le magasin a bien été ajouté."), 201

    elif request.method == 'PUT':
        try:
            store_id = request.form['id']
            store = Store.query.get_or_404(store_id)
            
            store.name = request.form['name']
            store.location = request.form['location']
            store.phone = request.form.get('phone')

            new_email = request.form['email']
            if store.email != new_email:
                store.email = new_email
                
                user = User.query.filter_by(email=store.email).first()
                if user:
                    user.email = new_email
                    db.session.add(user)

            logo_files = request.files.getlist('logo')
            if logo_files:
                logo_urls = save_files(logo_files, 'store_logos')
                store.logo_file_url = logo_urls[0] if logo_urls else store.logo_file_url

            db.session.commit()
            return jsonify(message="Les infos du magasin ont bien été mis à jour")

        except Exception as e:
            db.session.rollback()
            return jsonify(error=str(e)), 400

    elif request.method == 'DELETE':
        store_id = request.form['id']
        store = Store.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return jsonify(message="Le magasin a bien été retiré")


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


@main.route("/new_previouses")
@login_required
@employee_required
def new_quotes():
    quotes = Authorization.query.all()
    return render_template("dashboard/@support_team/quotes_list.html", quotes=quotes)

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
@ceo_required
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

        return jsonify({'success' : True, 'message' :  'Votre nouvelle campagne a été ajoutée, vous pouvez maintenant tirer le meilleur de votre audience' })

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
    employees = User.query.join(Role).filter(~Role.name.in_(['User', 'Reseller'])).all()
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

@main.route('/my_tasks')
@login_required
def my_tasks():
    user_email = current_user.email
    tasks = Task.query.filter_by(assigned_to=user_email).all()
    return render_template('dashboard/@support_team/my_task.html', tasks=tasks)