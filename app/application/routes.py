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
    """Creates an application in the database using the information entered by the form"""

    form = ApplicationForm()
    if request.method == 'POST':
        retrieved_application = find_application_by_name(form.name.data)

        if retrieved_application:
            flash('An application with this email address already exists within the system', category='error')
        elif form.validate_on_submit():
            try:
                new_application = Application(name=form.name.data , team_email=form.team_email.data,team_name=form.team_name.data,
                                              url=form.url.data, swagger=form.swagger.data, bitbucket=form.bitbucket.data,
                                              production_pods=form.production_pods.data, extra_info= form.extra_info.data)
                db.session.add(new_application)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to create application: %s', form.name.data)
                logging.error(err)
                flash('Unable to create application', category='error')
            else:
                logging.info('Application %s created successfully', form.name.data)
                flash('Application added successfully', category='success')

    return render_template('application/add-application.html', user=current_user, form=form)

@login_required
@application.route('/update', methods=['POST', 'GET'])
def update():
    """Updates an applications details in the database. This endpoint takes a query parameter of the applications id"""

    application_id = request.args.get('application_id')
    retrieved_application = find_application_by_id(application_id)
    form = ApplicationForm(obj = retrieved_application)

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
    """This function deletes and application from the database. This action can only be completed my admin user.
    This function takes a query parameter of the application id"""

    if request.method == 'GET' and current_user.is_admin:
        application_id = request.args.get('application_id')
        retrieved_application = find_application_by_id(application_id)
        if retrieved_application:
            try:
                db.session.delete(retrieved_application)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to delete application: %s', retrieved_application.name)
                logging.error(err)
                flash('Unable to delete application', category='error')
            else:
                logging.info('Application: %s deleted successfully', retrieved_application.name)
                flash('Application deleted successfully', category='success')
        else:
            flash('Application cannot be deleted as it does not exist', category='error')

    return redirect(url_for('views.dashboard'))

def find_application_by_id(application_id):
    """Find an application in the database using the applications id"""
    try:
        retrieved_application = Application.query.get(application_id)
        return retrieved_application
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Error occurred whilst querying the database')
        logging.error(err)

def find_application_by_name(name):
    """Finds an application in the database by the application name"""
    try:
        retrieved_application = Application.query.filter_by(name=name).first()
        return retrieved_application
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Error occurred whilst querying the database')
        logging.error(err)

@login_required
@application.route('/fetch_all', methods=['GET'])
def fetch_all_applications():
    return jsonify(db.session.query(Application).all())