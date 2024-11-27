import logging

from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.application import application
from app.application.forms import ApplicationForm
from app.models.application import Application
from app.models.server import Server


@login_required
@application.route('/create', methods=['GET', 'POST'])
def create():
    """Creates an application in the database using the information entered by the form"""
    form = ApplicationForm()
    form.server.choices = [(s.name, s.name) for s in Server.query.with_entities(Server.name)]
    form.server.choices.insert(0, ('Please Select', 'Please Select'))

    if request.method == 'POST':
        retrieved_application_by_name = find_application_by_name(form.name.data)
        retrieved_application_by_url = find_application_by_url(form.url.data)
        retrieved_application_by_bitbucket = find_application_by_bitbucket(form.bitbucket.data)

        if retrieved_application_by_name or retrieved_application_by_url or retrieved_application_by_bitbucket:
            flash('An application with this name, url or bitbucket already exists within the system', category='error')
        elif form.validate_on_submit():
            try:
                new_application = Application(name=form.name.data , team_email=form.team_email.data,team_name=form.team_name.data,
                                              url=form.url.data, swagger=form.swagger.data, bitbucket=form.bitbucket.data,
                                              production_pods=form.production_pods.data, extra_info= form.extra_info.data, server=form.server.data)
                db.session.add(new_application)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to create application: %s', form.name.data)
                logging.error(err)
                flash('Unable to create application', category='error')
            else:
                logging.info('Application %s added successfully', form.name.data)
                flash('Application added successfully', category='success')

    return render_template('application/add-application.html', user=current_user, form=form)

@login_required
@application.route('/update', methods=['POST', 'GET'])
def update():
    """Updates an applications details in the database. This endpoint takes a query parameter of the applications id"""

    application_id = request.args.get('application_id')
    retrieved_application = find_application_by_id(application_id)
    form = ApplicationForm(obj = retrieved_application)
    form.server.choices = [(s.name, s.name) for s in Server.query.with_entities(Server.name)]

    if request.method == 'POST':
        logging.info(form.data)
        retrieved_application_by_url = find_application_by_url(form.url.data)
        retrieved_application_by_bitbucket = find_application_by_bitbucket(form.bitbucket.data)

        if (retrieved_application_by_bitbucket and retrieved_application_by_bitbucket.id != retrieved_application.id) or (retrieved_application_by_url and retrieved_application_by_url.id != retrieved_application.id):
            flash('There is an application with the same bitbucket or url already in the system', category='error')
        elif form.validate_on_submit():
            updated_application = form.data
            updated_application.pop('csrf_token', None)
            if retrieved_application:
                try:
                    db.session.query(Application).filter_by(id=application_id).update(updated_application)
                    db.session.commit()
                except SQLAlchemyError as err:
                    db.session.rollback()
                    logging.error('Unable to update application: %s', updated_application['name'])
                    logging.error(err)
                    flash('Unable to update application', category='error')
                else:
                    logging.info('Application: %s successfully updated', updated_application['name'])
                    flash('Application successfully updated')
                    redirect(url_for('application.all_applications'))
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

    return redirect(url_for('application.all_applications'))

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

def find_application_by_url(url):
    """Finds an application in the database by the application url"""
    try:
        retrieved_application = Application.query.filter_by(url=url).first()
        return retrieved_application
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Error occurred whilst querying the database')
        logging.error(err)

def find_application_by_bitbucket(bitbucket):
    """Finds an application in the database by the application bitbucket url"""
    try:
        retrieved_application = Application.query.filter_by(bitbucket=bitbucket).first()
        return retrieved_application
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Error occurred whilst querying the database')
        logging.error(err)

@application.route('/all-applications')
@login_required
def all_applications():
    applications = db.session.query(Application).all()
    return render_template('application/grid.html', user=current_user, list=applications)