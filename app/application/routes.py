import logging

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.application import application
from app.application.forms import ApplicationForm
from app.models.application import Application
from app.models.server import Server, fetch_server_with_entity

@login_required
@application.route('/create', methods=['GET', 'POST'])
def create():
    """Creates an application in the database using the information entered by the form"""

    form = ApplicationForm()

    # Populating server dropdown with values from the server table
    servers = fetch_server_with_entity(Server.name)
    form.server.choices = [(s.name, s.name) for s in servers]
    form.server.choices.insert(0, ('Please Select', 'Please Select'))

    if request.method == 'POST':
        retrieved_application_by_name = find_application_by_name(form.name.data)
        retrieved_application_by_url = find_application_by_url(form.url.data)
        retrieved_application_by_bitbucket = find_application_by_bitbucket(form.bitbucket.data)

        #Check if new application has the same name, url or bitbucket an entry already in the database
        if retrieved_application_by_name or retrieved_application_by_url or retrieved_application_by_bitbucket:
            flash('An application with this name, url or bitbucket already exists within the system', category='error')
        #If the form is valid add application to database
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

        retrieved_application_by_url = find_application_by_url(form.url.data)
        retrieved_application_by_bitbucket = find_application_by_bitbucket(form.bitbucket.data)
        retrieved_application_by_name = find_application_by_name(form.name.data)

        # Checks if the updated application name, bitbucket or url conflicts with an existing entry in the database
        if (((retrieved_application_by_bitbucket and retrieved_application_by_bitbucket.id != retrieved_application.id)
             or (retrieved_application_by_url and retrieved_application_by_url.id != retrieved_application.id))
                or (retrieved_application_by_name and retrieved_application_by_name.id != retrieved_application.id)):
            flash('There is an application with the same name, bitbucket or url already in the system', category='error')
        # If form is valid update application information
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
                    flash('Application successfully updated', category='success')
                    redirect(url_for('application.all_applications'))
            else:
                flash('Application cannot be updated as it does not exist', category='error',)

    return render_template('application/update-application.html', user = current_user, application = retrieved_application, form = form)

@login_required
@application.route('/delete', methods=['GET', 'POST'])
def delete():
    """This function deletes and application from the database. This action can only be completed my admin user.
    This function takes a query parameter of the application id"""

    # Checks GET request was made to the endpoint and is user is an admin
    if request.method == 'GET' and current_user.is_admin:
        application_id = request.args.get('application_id')
        retrieved_application = find_application_by_id(application_id)
        #Deletes server
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

def find_application_by_id(id):
    """Find an application in the database using the applications id"""
    try:
        retrieved_application = Application.query.get(id)
        return retrieved_application
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('An error occurred whilst filtering the application table by id: %s', id)
        logging.error(err)

def find_application_by_name(name):
    """Finds an application in the database by the application name"""
    try:
        retrieved_application = Application.query.filter_by(name=name).first()
        return retrieved_application
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('An error occurred whilst filtering application table by name: %s', name)
        logging.error(err)

def find_application_by_url(url):
    """Finds an application in the database by the application url"""
    try:
        retrieved_application = Application.query.filter_by(url=url).first()
        return retrieved_application
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('An error occurred whilst filtering application table by url: %s', url)
        logging.error(err)

def find_application_by_bitbucket(bitbucket):
    """Finds an application in the database by the application bitbucket url"""
    try:
        retrieved_application = Application.query.filter_by(bitbucket=bitbucket).first()
        return retrieved_application
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('An error occurred whilst filtering application table by bitbucket: %s', bitbucket)
        logging.error(err)

def find_applications_deployed_on_server(server_name):
    """Fetches applications deployed on a server by searching for rows which has a
    server column equal to the parsed in server name"""
    try:
        returned_applications = Application.query.with_entities(Application.name).filter_by(server=server_name).all()
        results = [r for (r, ) in returned_applications]
        applications = ', '.join(name for name in results)
        return applications
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('An error occurred whilst querying the application table by entity: %s and filtering by server %s', (Application.name, server_name))
        logging.error(err)

def fetch_all_applications():
    """Fetches all applications in the application table"""
    try:
        applications = db.session.query(Application).all()
        return applications
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('An error occurred whilst fetching all rows in the application table')
        logging.error(err)

@application.route('/all-applications')
@login_required
def all_applications():
    """Renders the html for the grid to view all applications"""
    applications = fetch_all_applications()
    return render_template('application/grid.html', user=current_user, applications=applications)