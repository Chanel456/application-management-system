from flask import render_template, flash, request, url_for, redirect
from flask_login import login_required, current_user

from app.models.server import Server
from app.server import server
from app.server.forms import ServerForm


@server.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Creates a server in the database using the information entered by the form"""
    form = ServerForm()
    if request.method == 'POST':
        retrieved_server = Server.find_server_by_name(form.name.data)

        # Checking if server already exists in database with the same name
        if retrieved_server:
            flash('A server with this name already exists within the system', category='error')

        # If the create form is valid add server to database
        elif form.validate_on_submit():
            Server.create_server(form.name.data, form.cpu.data, form.memory.data, form.location.data)

    return render_template('server/add-server.html', user=current_user, form=form)

@server.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    """Updates a servers details in the database. This endpoint takes a query parameter of the server id"""

    server_id = request.args.get('server_id')
    retrieved_server = Server.find_server_by_id(server_id)
    form = ServerForm(obj=retrieved_server)

    if request.method == 'POST':
        retrieved_server_by_name = Server.find_server_by_name(form.name.data)

        # Checks if the updated server name conflicts with an existing entry in the database
        if retrieved_server_by_name and retrieved_server_by_name.id != retrieved_server.id:
            flash('There is a server with the same name already in the system', category='error')

        # If form is valid update server information
        elif form.validate_on_submit():
            updated_server = form.data
            updated_server.pop('csrf_token', None)
            if retrieved_server:
                Server.update_server(server_id, updated_server)
            else:
                message = f'Server {retrieved_server.name} cannot be updated as they do not exist'
                flash(message, category='error', )

    return render_template('server/update-server.html', user=current_user, form=form, server = retrieved_server)


@server.route('/delete', methods=['GET'])
@login_required
def delete():
    """This function deletes and server from the database. This action can only be completed my admin user.
        This function takes a query parameter of the server id"""

    # Checks GET request was made to the endpoint and is user is an admin
    if request.method == 'GET' and current_user.is_admin:
        server_id = request.args.get('server_id')
        retrieved_server = Server.find_server_by_id(server_id)
        applications_deployed_on_server = retrieved_server.applications

        # Checks if there are applications deployed on the server proposed to be deleted
        if applications_deployed_on_server:
            applications = ', '.join([app.name for app in applications_deployed_on_server])
            message = f'Server {retrieved_server.name} cannot be deleted as application(s) {applications} are running on it'
            flash(message, category='error')
        # Delete server
        elif retrieved_server:
            Server.delete_server(retrieved_server)
        else:
            message = f'Server {retrieved_server.name} cannot be deleted as it does not exist'
            flash(message, category='error')

    return redirect(url_for('server.all_servers'))

@server.route('/all-servers')
@login_required
def all_servers():
    """Renders the html for the grid to view all servers"""
    servers = Server.fetch_all_servers()
    return render_template('server/grid.html', user=current_user, list=servers)