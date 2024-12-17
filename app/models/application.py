import logging

from flask import flash
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError

from app import db

class Application(db.Model):
    """
        A class to represent the relational database table used to store the details of an application

        Columns
        -------------------
        id: integer
            application id
        name: string
            name of the application
        team_name: string
            Name of the team who is responsible for maintaining the application
        team_email: boolean
            Email address of the team responsible for maintaining the application
        url: string
            Url for the application
        bitbucket: string
            url for the bitbucket repo for the application
        extra_info: text
            Any extra information about the application
        production_pods: integer
            the number of pods this application has up in production
        server: string
            The server the application is deployed on
        """

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), unique = True)
    team_name = db.Column(db.String(150))
    team_email = db.Column(db.String(150))
    url = db.Column(db.String(200), unique=True)
    swagger = db.Column(db.String(200), nullable=True)
    bitbucket = db.Column(db.String(200), unique = True)
    extra_info = db.Column(db.Text(1000), nullable = True)
    production_pods = db.Column(db.Integer)
    server = db.Column(db.String(20), db.ForeignKey('server.name'))

    @staticmethod
    def find_application_by_id(id):
        """Find an application in the database using the applications id"""
        try:
            retrieved_application = Application.query.get(id)
            return retrieved_application
        except SQLAlchemyError as err:
            logging.error('An error occurred whilst filtering the application table by id: %s', id)
            logging.error(err)

    @staticmethod
    def find_application_by_name(name):
        """Finds an application in the database by the application name"""
        try:
            retrieved_application = Application.query.filter_by(name=name).first()
            return retrieved_application
        except SQLAlchemyError as err:
            logging.error('An error occurred whilst filtering application table by name: %s', name)
            logging.error(err)

    @staticmethod
    def find_application_by_url(url):
        """Finds an application in the database by the application url"""
        try:
            retrieved_application = Application.query.filter_by(url=url).first()
            return retrieved_application
        except SQLAlchemyError as err:
            logging.error('An error occurred whilst filtering application table by url: %s', url)
            logging.error(err)

    @staticmethod
    def find_application_by_bitbucket(bitbucket):
        """Finds an application in the database by the application bitbucket url"""
        try:
            retrieved_application = Application.query.filter_by(bitbucket=bitbucket).first()
            return retrieved_application
        except SQLAlchemyError as err:
            logging.error('An error occurred whilst filtering application table by bitbucket: %s', bitbucket)
            logging.error(err)


    @staticmethod
    def fetch_all_applications():
        """Fetches all applications in the application table"""
        try:
            applications = db.session.query(Application).all()
            return applications
        except SQLAlchemyError as err:
            logging.error('An error occurred whilst fetching all rows in the application table')
            logging.error(err)

    @staticmethod
    def create_application(name, team_name, team_email, url, swagger, bitbucket, production_pods, extra_info, server):
        """Creates a new application and adds it to the database"""
        try:
            new_application = Application(name=name, team_email=team_email, team_name=team_name, url=url, swagger=swagger,
                                          bitbucket=bitbucket,production_pods=production_pods, extra_info=extra_info,
                                          server=server)
            db.session.add(new_application)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            logging.error('Unable to create application: %s', name)
            logging.error(err)
            flash('Unable to create application', category='error')
        else:
            logging.info('Application %s added successfully', name)
            flash('Application added successfully', category='success')

    @staticmethod
    def update_application(application_id, updated_application):
        """Updates an existing application in the database"""
        try:
            db.session.query(Application).filter_by(id=application_id).update(updated_application)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            logging.error('An error was encountered when updating application with id: %s', application_id)
            logging.error(err)
            flash('Unable to update application', category='error')
        else:
            logging.info('Application: %s successfully updated', updated_application['name'])
            flash('Application successfully updated', category='success')


    @staticmethod
    def delete_application(application):
        """Deletes an application from the database"""
        try:
            db.session.delete(application)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            logging.error('An error was encountered when deleting application with id: %s', application.id)
            logging.error(err)
            flash('Unable to delete application', category='error')
        else:
            logging.info('Application: %s deleted successfully', application.name)
            flash('Application deleted successfully', category='success')


@event.listens_for(Application.__table__, 'after_create')
def create_applications(*args, **kwargs):
    """Inserting 10 rows of data into the application table after database creation"""
    try:
        db.session.add(Application(name='Example App One', team_name='Team One',
                                   team_email='team.one@gmail.com', url='https://exampleappone.com',
                                   swagger='https://exampleappone.com/swagger/ui',
                                   bitbucket='https://bitbucket.com/repos/exampleappone', extra_info='This is a Java application that uses the springboot framework.',
                                   production_pods=1, server='ab0001'))
        db.session.add(Application(name='Example App Two', team_name='Team Two',
                                   team_email='team.two@gmail.com', url='https://exampleapptwo.com',
                                   swagger='https://exampleapptwo.com/swagger/ui',
                                   bitbucket='https://bitbucket.com/repos/exampleapptwo', extra_info='',
                                   production_pods=2, server='ab0001'))
        db.session.add(Application(name='Example App Three', team_name='Team Three',
                                   team_email='team.three@gmail.com', url='https://exampleappthree.com',
                                   swagger='https://exampleappthree.com/swagger/ui',
                                   bitbucket='https://bitbucket.com/repos/exampleappthree', extra_info='',
                                   production_pods=3, server='ab0003'))
        db.session.add(Application(name='Example App Four', team_name='Team Four',
                                   team_email='team.four@gmail.com', url='https://exampleappfour.com',
                                   swagger='https://exampleappfour.com/swagger/ui',
                                   bitbucket='https://bitbucket.com/repos/exampleappfour', extra_info='',
                                   production_pods=2, server='ab0004'))
        db.session.add(Application(name='Example App Five', team_name='Team Five',
                                   team_email='team.five@gmail.com', url='https://exampleappfive.com',
                                   swagger='https://exampleappfive.com/swagger/ui',
                                   bitbucket='https://bitbucket.com/repos/exampleappfive', extra_info='',
                                   production_pods=1, server='ab0001'))
        db.session.add(Application(name='Example App Six', team_name='Team Six',
                                   team_email='team.six@gmail.com', url='https://exampleappsix.com',
                                   swagger='https://exampleappsix.com/swagger/ui',
                                   bitbucket='https://bitbucket.com/repos/exampleappsix', extra_info='',
                                   production_pods=3, server='ab0009'))
        db.session.add(Application(name='Example App Seven', team_name='Team Seven',
                                   team_email='team.seven@gmail.com', url='https://exampleappseven.com',
                                   swagger='',
                                   bitbucket='https://bitbucket.com/repos/exampleappseven', extra_info='This is an Angular application which uses Ngrx for state management',
                                   production_pods=1, server='ab0010'))
        db.session.add(Application(name='Example App Eight', team_name='Team Eight',
                                   team_email='team.eight@gmail.com', url='https://exampleappeight.com',
                                   swagger='https://exampleappeight.com/swagger/ui',
                                   bitbucket='https://bitbucket.com/repos/exampleappeight', extra_info='',
                                   production_pods=1, server='ab0005'))
        db.session.add(Application(name='Example App Nine', team_name='Team Nine',
                                   team_email='team.nine@gmail.com', url='https://exampleappnine.com',
                                   swagger='',
                                   bitbucket='https://bitbucket.com/repos/exampleappnine', extra_info='This is a React application that is used to manage loans',
                                   production_pods=2, server='ab0007'))
        db.session.add(Application(name='Example App Ten', team_name='Team Ten',
                                   team_email='team.ten@gmail.com', url='https://exampleappten.com',
                                   swagger='https://exampleappten.com/swagger/ui',
                                   bitbucket='https://bitbucket.com/repos/exampleappten', extra_info='',
                                   production_pods=1, server='ab0002'))
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.error('Unable to add dummy data to Application table on database creation')
        logging.error(err)