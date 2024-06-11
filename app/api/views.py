from flask import request, render_template, session,  flash, redirect, url_for, jsonify
from flask_babel import _
from . import api
from flask_login import current_user, login_required
from ..models import db, Event, Task, Note, Job, Employee, JobApplication, MarketingCampaign, Purchase, Authorization, Invoice
from ..decorators import ceo_required, hr_manager_required, user_required, sales_manager_required, accountant_required, employee_required
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import secrets
from .utils import save_files, generate_qr_code, save_authorization_request_files
import json
from dotenv import load_dotenv
import os, requests

load_dotenv()


@api.route("/quotes/apply", methods=['GET', 'POST'])
@login_required
@user_required
def apply_quotes():
    if request.method == 'POST':
        client_first_name = request.form.get('client_first_name')
        client_last_name = request.form.get('client_last_name')
        client_phone_number = request.form.get('client_phone_number')
        client_location = request.form.get('client_location')
        lading_number = request.form.get('lading_number')
        agent_first_name = request.form.get('agent_first_name')
        agent_last_name = request.form.get('agent_last_name')
        shipping_company_title = request.form.get('shipping_company_title')
        
        client_signature_file = request.files.get('client_signature_url')
        client_id_file = request.files.get('client_id_card_url')

        try:
            saved_files = save_authorization_request_files([client_signature_file, client_id_file], client_first_name, client_last_name)
            client_signature_url = saved_files[0] if len(saved_files) > 0 else ''
            client_id_card_url = saved_files[1] if len(saved_files) > 1 else ''

            qr_code_path = generate_qr_code(lading_number, client_first_name, client_last_name)

            new_authorization = Authorization(
                client_first_name=client_first_name,
                client_last_name=client_last_name,
                client_phone_number=client_phone_number,
                client_location=client_location,
                lading_bills_identifier=lading_number,
                agent_first_name=agent_first_name,
                agent_last_name=agent_last_name,
                shipping_company_title=shipping_company_title,
                client_signature_url=client_signature_url,
                client_id_card_url=client_id_card_url,
                user_id=current_user.id
            )

            db.session.add(new_authorization)
            db.session.commit()

            return jsonify({'success': True, 'message': _('Votre requête a bien été envoyé')}), 200

        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    return render_template('api/customers/authorizations/apply.html')



@api.route("/my_purchases/track_my_product/user", methods=['GET'])
def get_user_purchases():
    user_id = current_user.id if current_user.is_authenticated else None
    purchases = Purchase.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'token': purchase.token,
        'title': purchase.title
    } for purchase in purchases])


@api.route("/purchases/request", methods=['GET', 'POST'])
@login_required
@user_required
def purchase_request():
    if request.method == 'POST':
        data = request.form
        files = request.files

        token = secrets.token_urlsafe(16)

        product_picture_paths = save_files(files.getlist('product_picture_url'), data['author_first_name'], data['author_last_name'])
        doc_paths = save_files(files.getlist('doc_url'), data['author_first_name'], data['author_last_name'])

        purchase = Purchase(
            title=data['title'],
            author_first_name=data['author_first_name'],
            author_last_name=data['author_last_name'],
            author_address=data['author_address'],
            author_email_address=data['author_email_address'],
            product_length=float(data.get('product_length', 0.0)),
            product_width=float(data.get('product_width', 0.0)),
            author_phone_number=data['author_phone_number'],
            location=data['location'],
            provider=data.get('provider'),
            product_picture_url=json.dumps(product_picture_paths),
            description=data['description'],
            category=data['category'],
            doc_url=json.dumps(doc_paths),
            user_id=current_user.id,
            token=token,
            qr_code_url=generate_qr_code(token, data['author_first_name'], data['author_last_name']),
            start_check=datetime.utcnow()
        )

        db.session.add(purchase)
        
        try:
            db.session.commit()
            
            return jsonify({
                'title': _('Envoyé avec succès'), 
                'message': _('Votre requête a été bien envoyé'), 
                'token': token
            })
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return render_template('api/customers/goods/purchase_request.html')

@api.route("/mailbox/new_message")
@login_required
def new_message():
    return render_template('api/messages/new_message.html')

@api.route("/notes/create_notice", methods=["GET", "POST"])
@login_required
def add_notes():
    if request.method == "POST":
        title = request.form.get('title')
        nature = request.form.get('nature')
        content = request.form.get('content')
        
        new_note = Note(
            title=title,
            content=content,
            nature=nature
        )
        db.session.add(new_note)
        db.session.commit()
        
        return jsonify({'success': True})

    return render_template('api/@support_team/notice/create_notice.html')


@api.route("/careers/add_a_job", methods=["GET", "POST"])
@login_required
@hr_manager_required
def create_job():
    if request.method == "POST":
        try:
            data = request.get_json(force=True)
        except Exception as e:
            return jsonify({"success": False, "message": "Invalid JSON payload"}), 400

        title = data.get('title')
        description = data.get('description')
        location = data.get('location')
        salary = data.get('salary')
        posted_date_str = data.get('posted_date')
        closing_date_str = data.get('closing_date')
        
        errors = []
        if not title:
            errors.append("Le titre est requis.")
        if not description:
            errors.append("La description est requise.")
        if not location:
            errors.append("Le lieu est requis.")
        if not salary:
            errors.append("Le salaire est requis.")
        if not posted_date_str:
            errors.append("La date de publication est requise.")
        if not closing_date_str:
            errors.append("La date de clôture est requise.")
        
        if errors:
            return jsonify({"success": False, "message": " ".join(errors)}), 400
        
        try:
            posted_date = datetime.strptime(posted_date_str, '%Y-%m-%d')
            closing_date = datetime.strptime(closing_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"success": False, "message": "Dates invalides."}), 400
        
        job = Job(
            title=title,
            description=description,
            location=location,
            salary=salary,
            posted_date=posted_date,
            closing_date=closing_date
        )
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({"success": True, "message": "Offre d'emploi créée avec succès!"}), 200
    
    return render_template('api/@support_team/jobs/create_job.html')
    
@api.route("/add_event", methods=['POST'])
@login_required
@ceo_required
def add_event():
    title = request.form.get('title')
    status = request.form.get('status')
    start_from = request.form.get('start_from')
    end_at = request.form.get('end_at')
    report = request.form.get('report')

    try:
        start_from = datetime.fromisoformat(start_from)
        end_at = datetime.fromisoformat(end_at)
    except ValueError as e:
        flash(f"Invalid date format: {e}", "danger")
        return redirect(url_for('main.events'))

    new_event = Event(
        title=title,
        status=status,
        start_from=start_from,
        end_at=end_at,
        report=report
    )

    db.session.add(new_event)
    db.session.commit()

    flash('Événement ajouté avec succès!', 'success')
    return redirect(url_for('main.events'))

@api.route('/my_purchases/delete/<int:purchase_id>', methods=['DELETE'])
@user_required
@login_required
def delete_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    if purchase.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403

    db.session.delete(purchase)
    try:
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api.route("/docs/create_new_document")
@login_required
def create_doc():
    return render_template('api/docs/text_doc.html')

@api.route("/docs/create_new_spreadsheet")
@login_required
def create_spreadsheet():
    return render_template('api/docs/spreadsheet_doc.html')

@api.route("/manage/task/<int:task_id>", methods=["GET", "POST", "DELETE", "PUT"])
@login_required
@ceo_required
def manage_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'GET':
        return jsonify({'success': True, 'task': {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'assigned_to': task.assigned_to
        }})

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.assigned_to = request.form.get('assigned_to')
        db.session.commit()

        return jsonify({'success': True})

    if request.method == 'PUT':
        data = request.get_json(force=True)
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.assigned_to = data.get('assigned_to', task.assigned_to)
        db.session.commit()

        return jsonify({'success': True})

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()

        return jsonify({'success': True})
    
@api.route("/manage/note/<int:note_id>", methods=["GET", "POST", "DELETE", "PUT"])
@login_required
@ceo_required
def manage_note(note_id):
    note = Note.query.get_or_404(note_id)

    if request.method == 'GET':
        return jsonify({'success': True, 'note': {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'nature': note.nature
        }})

    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form.get('content')
        note.nature = request.form.get('nature')
        db.session.commit()
        return jsonify({'success': True})

    if request.method == 'PUT':
        data = request.get_json(force=True)
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        note.nature = data.get('nature', note.nature)
        db.session.commit()
        return jsonify({'success': True})

    if request.method == 'DELETE':
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True})


@api.route("/careers/edit_job/<int:job_id>", methods=["GET", "POST"])
@login_required
@hr_manager_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == "POST":
        job.title = request.form['title']
        job.description = request.form['description']
        job.location = request.form['location']
        job.salary = request.form['salary']
        job.posted_date = datetime.strptime(request.form['posted_date'], '%Y-%m-%d')
        job.closing_date = datetime.strptime(request.form['closing_date'], '%Y-%m-%d')
        db.session.commit()
        flash(_('Offre mise à jour avec succès'), 'success')
        return redirect(url_for('main.previous_created_jobs'))
    return render_template('api/@support_team/jobs/edit_job.html', job=job)

@api.route("/careers/delete_job/<int:job_id>", methods=["DELETE"])
@login_required
@hr_manager_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({'success' : True})
    

@api.route("/careers/employees/edit_employee_infos/<int:employee_id>", methods=["GET", "POST"])
@login_required
@hr_manager_required
def edit_employee_infos(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    
    if request.method == "POST":
        data = request.get_json()
        employee.employee_first_name = data.get('employee_first_name')
        employee.employee_last_name = data.get('employee_last_name')
        employee.employee_job_title = data.get('employee_job_title')
        employee.identifier = data.get('employee_identifier')
        
        try:
            db.session.commit()
            return jsonify(success=True, message='Les informations ont été mises à jour avec succès.')
        except Exception as e:
            db.session.rollback()
            return jsonify(success=False, message=f'Erreur lors de la mise à jour: {str(e)}')
    
    return render_template('api/@support_team/employees/edit_employee_infos.html', employee=employee)

@api.route("/careers/employees/delete_employee/<int:employee_id>", methods=["DELETE"])
@login_required
@hr_manager_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    try:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
@api.route("/careers/submit_application", methods=["POST"])
@login_required
def submit_application():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    location = request.form['location']
    motivation = request.form['motivation']
    linkedin = request.form['linkedin']
    github = request.form['github']
    dribble = request.form['dribble']
    date_of_birth = request.form['date_of_birth']
    cv = request.files['cv']
    
    cv_url = f"/static/uploads/{cv.filename}"
    cv.save(f"app/static/uploads/{cv.filename}")

    application = JobApplication(
        applicant_first_name=first_name,
        applicant_last_name=last_name,
        applicant_email_address=email,
        applicant_location=location,
        motivation=motivation,
        linkedin_url=linkedin,
        github_url=github,
        dribble_url=dribble,
        date_of_birth=date_of_birth,
        CV_url=cv_url,
        user_id=current_user.id,
        job_id=1 
    )
    db.session.add(application)
    db.session.commit()

    flash(_('Votre candidature a été soumise avec succès!'), 'success')
    return redirect(url_for('main.my_recent_applications'))

@api.route('/edit_ad/<int:ad_id>', methods=['POST'])
@login_required
def edit_ad(ad_id):
    ad = MarketingCampaign.query.get_or_404(ad_id)
    data = request.json

    title = data.get('title')
    description = data.get('description')
    objectives = data.get('objectives')
    start_from = data.get('start_from')
    end_at = data.get('end_at')
    min_budget = data.get('min_budget')
    max_budget = data.get('max_budget')
    debt = data.get('debt')

    try:
        if not isinstance(start_from, str):
            start_from = str(start_from)
        if not isinstance(end_at, str):
            end_at = str(end_at)
            
        ad.title = title
        ad.description = description
        ad.objectives = objectives
        ad.start_from = datetime.fromisoformat(start_from)
        ad.end_at = datetime.fromisoformat(end_at)
        ad.min_budget = float(min_budget)
        ad.max_budget = float(max_budget)
        ad.debt = float(debt)

        db.session.commit()
        return jsonify({'success': True, 'message': _('Votre campagne a été bien mise à jour')}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    

@api.route('/ads/delete_ad/<int:ad_id>', methods=['DELETE'])
@login_required
def delete_ad(ad_id):
    ad = MarketingCampaign.query.get_or_404(ad_id)
    try:
        db.session.delete(ad)
        db.session.commit()
        return jsonify({'success': True, 'message': _('Campagne supprimée')}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    

@api.route('/edit_request/<int:request_id>', methods=['POST'])
@login_required
def edit_request(request_id):
    req = Authorization.query.get_or_404(request_id)
    if req.user_id != current_user.id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    req.client_first_name = request.form.get('client_first_name')
    req.client_last_name = request.form.get('client_last_name')
    req.client_phone_number = request.form.get('client_phone_number')
    req.client_location = request.form.get('client_location')
    req.lading_bills_identifier = request.form.get('lading_number')
    req.agent_first_name = request.form.get('agent_first_name')
    req.agent_last_name = request.form.get('agent_last_name')
    req.shipping_company_title = request.form.get('shipping_company_title')

    files = []
    if 'client_signature_url' in request.files:
        files.append(request.files['client_signature_url'])
    if 'client_id_card_url' in request.files:
        files.append(request.files['client_id_card_url'])

    if files:
        save_authorization_request_files(files, req.client_first_name, req.client_last_name)

    db.session.commit()
    return jsonify({"success": True, "message": _("Votre demande a bien été mise à jour")})

@api.route('/delete_request/<int:request_id>', methods=['DELETE'])
@login_required
def delete_request(request_id):
    req = Authorization.query.get_or_404(request_id)
    if req.user_id != current_user.id:
        return jsonify({"success": False, "message": _("Accès non autorisé")}), 403

    db.session.delete(req)
    db.session.commit()
    return jsonify({"success": True, "message": _("Votre demande a été bien supprimé")})

@api.route('/delete_purchase/<int:purchase_id>', methods=['DELETE'])
@login_required
@sales_manager_required
def delete_client_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    if purchase is None:
        return jsonify({'message': 'Purchase not found'}), 404

    try:
        db.session.delete(purchase)
        db.session.commit()
        return jsonify({'message': 'Commande supprimée'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erreur lors de la suppression', 'error': str(e)}), 500
    

@api.route("/edit_invoice/<int:invoice_id>", methods=['PUT'])
@login_required
@accountant_required
def edit_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    if not invoice:
        return jsonify({'message': _('La facture est introuvable.')}), 404

    data = request.get_json()
    title = data.get('title')
    amount = data.get('amount')
    description = data.get('description')

    if not title or not amount:
        return jsonify({'message': _('Le titre et le montant sont requis.')}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        return jsonify({'message': _('Montant invalide.')}), 400

    invoice.title = title
    invoice.amount = amount
    invoice.description = description
    db.session.commit()

    return jsonify({'message': _('La facture a été mise à jour avec succès.')}), 200


@api.route("/delete_invoice/<int:invoice_id>", methods=['DELETE'])
@login_required
@accountant_required
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    if not invoice:
        return jsonify({'message': _('La facture est introuvable.')}), 404

    try:
        db.session.delete(invoice)
        db.session.commit()
        return jsonify({'message': _('La facture a été supprimée avec succès.')}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': _('Une erreur est survenue lors de la suppression de la facture.')}), 500
    

@api.route('/quote/delete/<int:quote_id>', methods=['DELETE'])
@login_required
@employee_required
def delete_quote(quote_id):
    quote = Authorization.query.get_or_404(quote_id)
    if quote:
        db.session.delete(quote)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': _('Demande Introuvable')}), 404

@api.route('/quote/edit/<int:quote_id>', methods=['PUT'])
@login_required
@employee_required
def edit_quote(quote_id):
    quote = Authorization.query.get_or_404(quote_id)
    if not quote:
        return jsonify({'success': False, 'message': _('Demande Introuvable')}), 404

    data = request.json
    if 'client_first_name' in data:
        quote.client_first_name = data['client_first_name']
    if 'client_last_name' in data:
        quote.client_last_name = data['client_last_name']
    if 'client_phone_number' in data:
        quote.client_phone_number = data['client_phone_number']
    if 'client_email_adress' in data:
        quote.client_email_adress = data['client_email_adress']
    if 'shipping_company_title' in data:
        quote.shipping_company_title = data['shipping_company_title']
    if 'lading_bills_identifier' in data:
        quote.lading_bills_identifier = data['lading_bills_identifier']
    if 'service_fees' in data:
        quote.service_fees = data['service_fees']

    db.session.commit()
    return jsonify({'success': True})

# geocoding api
@api.route("/autocomplete-address", methods=["GET"])
def autocomplete_address():
    query = request.args.get("query")
    key = os.environ.get('OPENCAGE_API_KEY')
    url = f"https://api.opencagedata.com/geocode/v1/json?q={query}&key={key}"
    
    response = requests.get(url)
    data = response.json()

    suggestions = []
    if data["results"]:
        for result in data["results"]:
            suggestions.append(result["formatted"])

    return jsonify(suggestions)


@api.route('/get-air-freight-rate', methods=['POST'])
def get_air_freight_rate():
    data = request.get_json()

    request_url = "https://sandbox.freightos.com/api/v1/freightEstimates"

    request_headers = {
        "x-apikey": os.environ.get('FREIGHTOS_API_KEY'),
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    request_body = {
        "legs": [
            {
                "origin": data['DepartPort'],
                "destination": data['Arrival'],
                "date": data['Date']
            }
        ],
        "load": {
            "weight": {"value": data['Weight'], "unit": "kg"} if data['Weight'] else None,
            "volume": {"value": data['Volume'], "unit": "m3"} if data['Volume'] else None,
            "dimensions": {
                "length": {"value": data['Length'], "unit": "m"},
                "width": {"value": data['Width'], "unit": "m"},
                "height": {"value": data['Height'], "unit": "m"}
            } if data['Length'] and data['Width'] and data['Height'] else None
        }
    }

    request_body['load'] = {k: v for k, v in request_body['load'].items() if v is not None}

    response = requests.post(request_url, headers=request_headers, json=request_body)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch rates', 'details': response.text}), response.status_code


# weather api
@api.route("/get-location")
def get_location():
    ip_info_url = "http://ipinfo.io/json"
    response = requests.get(ip_info_url)
    data = response.json()
    return jsonify(data)

@api.route("/get-weather/infos", methods=['GET'])
def get_weather():
    tomorrow_api_key = os.environ.get('TOMORROW_API_KEY')
    ip_info_url = "http://ipinfo.io/json"
    response = requests.get(ip_info_url)
    location_data = response.json()
    location = location_data['loc'] 

    tomorrow_api_key = os.environ.get('TOMORROW_API_KEY')
    weather_url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={tomorrow_api_key}"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    return jsonify(weather_data)
