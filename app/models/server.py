import logging

from flask import flash
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError

from app import db

class Server (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique= True)
    cpu = db.Column(db.Integer)
    memory = db.Column(db.Integer)
    location = db.Column(db.String(50))
    applications = db.relationship('Application')

    @staticmethod
    def fetch_server_with_entity(entity):
        try:
            result = Server.query.with_entities(entity)
            return result
        except SQLAlchemyError as err:
            logging.error('An error occurred whilst querying the server table with entity: %s', entity)
            logging.error(err)

    @staticmethod
    def find_server_by_id(server_id):
        """Find a server in the database using the server id"""
        try:
            retrieved_server = Server.query.get(server_id)
            return retrieved_server
        except SQLAlchemyError as err:
            logging.error('An error occurred whilst finding server by id: %s', server_id)
            logging.error(err)

    @staticmethod
    def find_server_by_name(name):
        """Finds a server in the database by the server name"""
        try:
            retrieved_server = Server.query.filter_by(name=name).first()
            return retrieved_server
        except SQLAlchemyError as err:
            logging.error('An error occurred whilst finding server by name: %s', name)
            logging.error(err)

    @staticmethod
    def fetch_all_servers():
        """Fetches all servers in the server table"""
        try:
            servers = db.session.query(Server).all()
            return servers
        except SQLAlchemyError as err:
            logging.error('An error occurred whilst fetching all rows in the server table')
            logging.error(err)

    @staticmethod
    def create_server(name, cpu, memory, location):
        """Creates a new server and adds it to the database"""
        try:
            new_server = Server(name=name, cpu=cpu, memory=memory, location=location)
            db.session.add(new_server)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            logging.error('Unable to create server: %s', name)
            logging.error(err)
            flash('Unable to create server', category='error')
        else:
            logging.info('Server %s added successfully', name)
            flash('Server added successfully', category='success')

    @staticmethod
    def update_server(server_id, updated_server):
        """Updates an existing server in the database"""
        try:
            db.session.query(Server).filter_by(id=server_id).update(updated_server)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            logging.error('An error was encountered when updating application with id: %s', server_id)
            logging.error(err)
            flash('Unable to update server', category='error')
        else:
            logging.info('Server: %s successfully updated', updated_server['name'])
            flash('Server successfully updated', category='success')

    @staticmethod
    def delete_server(server):
        """Deletes a server from the database"""
        try:
            db.session.delete(server)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            logging.error('An error was encountered when deleting server with id: %s', server.id)
            logging.error(err)
            flash('Unable to delete server', category='error')
        else:
            logging.info('Server: %s deleted successfully', server.name)
            flash('Server deleted successfully', category='success')



@event.listens_for(Server.__table__, 'after_create')
def create_servers(*args, **kwargs):
    """Inserting 10 rows of data into server table on after database creation"""
    try:
        db.session.add(Server(name='ab0001', cpu=123, memory=123, location='Walthamstow'))
        db.session.add(Server(name='ab0002', cpu=234, memory=234, location='Harrow'))
        db.session.add(Server(name='ab0003', cpu=345, memory=345, location='Walthamstow'))
        db.session.add(Server(name='ab0004', cpu=456, memory=456, location='Walthamstow'))
        db.session.add(Server(name='ab0005', cpu=567, memory=567, location='Harrow'))
        db.session.add(Server(name='ab0006', cpu=678, memory=678, location='Walthamstow'))
        db.session.add(Server(name='ab0007', cpu=789, memory=789, location='Walthamstow'))
        db.session.add(Server(name='ab0008', cpu=890, memory=890, location='Harrow'))
        db.session.add(Server(name='ab0009', cpu=901, memory=901, location='Walthamstow'))
        db.session.add(Server(name='ab0010', cpu=184, memory=184, location='Walthamstow'))
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Unable to add dummy data to Server table on database creation')
        logging.error(err)