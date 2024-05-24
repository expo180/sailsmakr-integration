from flask import request, render_template, session,  flash, redirect, url_for, jsonify
from flask_babel import _
from . import api
from flask_login import current_user, login_required
from ..models import db, Event, Task, Note, Job, Employee, JobApplication, MarketingCampaign
from ..decorators import ceo_required, hr_manager_required
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

@api.route("/quotes/apply")
def apply_quotes():
    return render_template('api/customers/authorizations/apply.html')

@api.route("/purchases/request")
@login_required
def purchase_request():
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