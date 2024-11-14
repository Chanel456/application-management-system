import logging

from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.application import application
from app.application.forms import ApplicationForm
from app.models.application import Application

@login_required
@application.route('/create', methods=['GET', 'POST'])
def create():
    form = ApplicationForm()
    if request.method == 'POST':
        retrieved_application = find_application_by_name(form.name.data)

        if retrieved_application:
            flash('An application with this email address already exists within the system', category='error')
        elif form.validate_on_submit():
            try:
                new_application = Application(name=form.name.data, owner_id=current_user.id , team_email=form.team_email.data,
                                        team_name=form.team_name.data, url=form.url.data, swagger_link=form.swagger_link.data, status=form.status.data)
                db.session.add(new_application)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to create application: %s, {err}', form.name.data)
                flash('Unable to create application', category='error')
            else:
                logging.info('Application %s created successfully', form.name.data)
                flash('Application added successfully', category='success')

    return render_template('application/add-application.html', user=current_user, form=form)

@login_required
@application.route('/update', methods=['POST', 'GET'])
def update():
    form = ApplicationForm()
    application_id = request.args.get('application_id')
    retrieved_application = find_application_by_id(application_id)
    if request.method == 'POST' and form.validate_on_submit():
        updated_application = form.data
        updated_application.pop('csrf_token', None)
        if retrieved_application:
            try:
                db.session.query(Application).filter_by(application_id=application_id).update(updated_application)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to update application: %s', updated_application['name'])
                logging.error(err)
                flash('Unable to update application', category='error')
            else:
                logging.info('Application: %s successfully updated', updated_application['name'])
                flash('Application successfully updated')
                redirect(url_for('views.dashboard'))
        else:
            flash('Application cannot be updated as they do not exist', category='error',)

    return render_template('application/update-application.html', user = current_user, application = retrieved_application, form = form)

@login_required
@application.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'GET' and current_user.is_admin:
        application_id = request.args.get('application_id')
        retrieved_application = find_application_by_id(application_id)
        if retrieved_application:
            try:
                db.session.delete(retrieved_application)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to delete application: %s {err}', retrieved_application.name)
                flash('Unable to delete application', category='error')
            else:
                logging.info('Application: %s deleted successfully', retrieved_application.name)
                flash('Application deleted successfully', category='success')
        else:
            flash('Application cannot be deleted as it does not exist', category='error')

    return redirect(url_for('views.dashboard'))

def find_application_by_id(application_id):
    try:
        retrieved_application = Application.query.get(application_id)
        return retrieved_application
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Error occurred whilst querying the database {err}')

def find_application_by_name(name):
    try:
        retrieved_application = Application.query.filter_by(name=name).first()
        return retrieved_application
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Error occurred whilst querying the database {err}')

# see if i need these endpoints, i might remove.
@login_required
@application.route('/fetch_all', methods=['GET'])
def fetch_all_applications():
    return jsonify(db.session.query(Application).all())
