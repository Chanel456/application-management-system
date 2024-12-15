from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.application import application
from app.application.forms import ApplicationForm
from app.models.application import Application
from app.models.server import Server

@login_required
@application.route('/create', methods=['GET', 'POST'])
def create():
    """Creates an application in the database using the information entered by the form"""

    form = ApplicationForm()

    # Populating server dropdown with values from the server table
    servers = Server.fetch_server_with_entity(Server.name)
    form.server.choices = [(s.name, s.name) for s in servers]
    form.server.choices.insert(0, ('Please Select', 'Please Select'))

    if request.method == 'POST':
        retrieved_application_by_name = Application.find_application_by_name(form.name.data)
        retrieved_application_by_url = Application.find_application_by_url(form.url.data)
        retrieved_application_by_bitbucket = Application.find_application_by_bitbucket(form.bitbucket.data)

        #Check if new application has the same name, url or bitbucket an entry already in the database
        if retrieved_application_by_name or retrieved_application_by_url or retrieved_application_by_bitbucket:
            flash('An application with this name, url or bitbucket already exists within the system', category='error')

        #If the form is valid add application to database
        elif form.validate_on_submit():
            Application.create_application(form.name.data, form.team_name.data, form.team_email.data, form.url.data,
                                           form.swagger.data, form.bitbucket.data, form.production_pods.data,
                                           form.extra_info.data, form.server.data)

    return render_template('application/add-application.html', user=current_user, form=form)

@login_required
@application.route('/update', methods=['POST', 'GET'])
def update():
    """Updates an applications details in the database. This endpoint takes a query parameter of the applications id"""

    application_id = request.args.get('application_id')
    retrieved_application = Application.find_application_by_id(application_id)
    form = ApplicationForm(obj = retrieved_application)
    form.server.choices = [(s.name, s.name) for s in Server.query.with_entities(Server.name)]

    if request.method == 'POST':

        retrieved_application_by_url = Application.find_application_by_url(form.url.data)
        retrieved_application_by_bitbucket = Application.find_application_by_bitbucket(form.bitbucket.data)
        retrieved_application_by_name = Application.find_application_by_name(form.name.data)

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
                Application.update_application(application_id, updated_application)
            else:
                message = f'Application {retrieved_application.name} cannot be updated as they do not exist'
                flash(message, category='error',)

    return render_template('application/update-application.html', user = current_user, application = retrieved_application, form = form)

@login_required
@application.route('/delete', methods=['GET', 'POST'])
def delete():
    """This function deletes and application from the database. This action can only be completed my admin user.
    This function takes a query parameter of the application id"""

    # Checks GET request was made to the endpoint and is user is an admin
    if request.method == 'GET' and current_user.is_admin:
        application_id = request.args.get('application_id')
        retrieved_application = Application.find_application_by_id(application_id)

        #Deletes server
        if retrieved_application:
            Application.delete_application(retrieved_application)
        else:
            message = f'Application {retrieved_application} cannot be deleted as it does not exist'
            flash(message, category='error')

    return redirect(url_for('application.all_applications'))

@application.route('/all-applications')
@login_required
def all_applications():
    """Renders the html for the grid to view all applications"""
    applications = Application.fetch_all_applications()
    return render_template('application/grid.html', user=current_user, applications=applications)