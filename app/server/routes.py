import logging

from flask import jsonify, render_template, flash, request, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.server import Server
from app.server import server
from app.server.forms import ServerForm


@server.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Creates a server in the database using the information entered by the form"""
    form = ServerForm()
    if request.method == 'POST':
        retrieved_server = find_server_by_name(form.name.data)
        logging.info(form.data)

        if retrieved_server:
            flash('A server with this name already exists within the system', category='error')
        elif form.validate_on_submit():
            try:
                new_server = Server(name=form.name.data, cpu=form.cpu.data,
                                              memory=form.memory.data,
                                              location=form.location.data, )
                db.session.add(new_server)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to create server: %s', form.name.data)
                logging.error(err)
                flash('Unable to create server', category='error')
            else:
                logging.info('Server %s added successfully', form.name.data)
                flash('Server added successfully', category='success')

    return render_template('server/add-server.html', user=current_user, form=form)

@server.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    """Updates a servers details in the database. This endpoint takes a query parameter of the server id"""

    server_id = request.args.get('server_id')
    retrieved_server = find_server_by_id(server_id)
    form = ServerForm(obj=retrieved_server)

    if request.method == 'POST' and form.validate_on_submit():
        updated_server = form.data
        updated_server.pop('csrf_token', None)
        if retrieved_server:
            try:
                db.session.query(Server).filter_by(id=server_id).update(updated_server)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to update server: %s', updated_server['name'])
                logging.error(err)
                flash('Unable to update server', category='error')
            else:
                logging.info('Server: %s successfully updated', updated_server['name'])
                flash('Server successfully updated')
                redirect(url_for('server.all_servers'))
        else:
            flash('Server cannot be updated as they do not exist', category='error', )

    return render_template('server/update-server.html', user=current_user, form=form, server = retrieved_server)


@server.route('/delete', methods=['GET'])
@login_required
def delete():
    """This function deletes and server from the database. This action can only be completed my admin user.
        This function takes a query parameter of the server id"""

    if request.method == 'GET' and current_user.is_admin:
        server_id = request.args.get('server_id')
        retrieved_server = find_server_by_id(server_id)
        if retrieved_server:
            try:
                db.session.delete(retrieved_server)
                db.session.commit()
            except SQLAlchemyError as err:
                db.session.rollback()
                logging.error('Unable to delete server: %s', retrieved_server.name)
                logging.error(err)
                flash('Unable to delete server', category='error')
            else:
                logging.info('Server: %s deleted successfully', retrieved_server.name)
                flash('Server deleted successfully', category='success')
        else:
            flash('Server cannot be deleted as it does not exist', category='error')

    return redirect(url_for('server.all_servers'))

def find_server_by_id(server_id):
    """Find a server in the database using the server id"""
    try:
        retrieved_server = Server.query.get(server_id)
        return retrieved_server
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Error occurred whilst querying the database')
        logging.error(err)

def find_server_by_name(name):
    """Finds a server in the database by the server name"""
    try:
        retrieved_server = Server.query.filter_by(name=name).first()
        return retrieved_server
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Error occurred whilst querying the database')
        logging.error(err)

@server.route('/all-servers')
@login_required
def all_servers():
    servers = db.session.query(Server).all()
    return render_template('server/grid.html', user=current_user, list=servers)


@login_required
@server.route('/fetch_all_servers', methods=['GET'])
def fetch_all_servers():
    return jsonify(db.session.query(Server).all())
