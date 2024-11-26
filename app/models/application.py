import datetime
from dataclasses import dataclass

from app import db

@dataclass
class Application(db.Model):
    """
        A class to represent the relational database table used to store the details of an application

        Columns
        -------------------
        id: int
            application id
        name: str
            name of the application
        team_name: str
            Name of the team who is responsible for maintaining the application
        team_email: boolean
            Email address of the team responsible for maintaining the application
        url: str
            Url for the application
        bitbucket: str
            url for the bitbucket repo for the application
        extra_info: str
            Any extra information about the application
        production_pods: int
            the number of pods this application has up in production
        server: string
            The server the application is deployed on
        created: datetime
            The time this record was created
        """

    id: int = db.Column(db.Integer, primary_key = True)
    name: str = db.Column(db.String(150), unique = True)
    team_name: str = db.Column(db.String(150))
    team_email: str = db.Column(db.String(150))
    url: str = db.Column(db.String(150))
    swagger: str = db.Column(db.String(150), nullable=True)
    bitbucket: str = db.Column(db.String(200), unique = True)
    extra_info: str = db.Column(db.Text(200), nullable = True)
    production_pods: int = db.Column(db.Integer)
    server: str = db.Column(db.String(150))
    created: datetime.datetime= db.Column(db.DateTime, default=datetime.datetime.now())

def create_applications(*args, **kwargs):
    db.session.add(Application(name='Example App One', team_name='Team One',
                               team_email='team.one@gmail.com', url='https://exampleappone.com',
                               swagger='https://exampleappone.com/swagger/ui',
                               bitbucket='https://bitbucket.com/repos/exampleappone', extra_info=None,
                               production_pods=1, server='ab0001'))
    db.session.add(Application(name='Example App Two', team_name='Team Two',
                               team_email='team.two@gmail.com', url='https://exampleapptwo.com',
                               swagger='https://exampleapptwo.com/swagger/ui',
                               bitbucket='https://bitbucket.com/repos/exampleapptwo', extra_info=None,
                               production_pods=2, server='ab0001'))
    db.session.add(Application(name='Example App Three', team_name='Team Three',
                               team_email='team.three@gmail.com', url='https://exampleappthree.com',
                               swagger='https://exampleappthree.com/swagger/ui',
                               bitbucket='https://bitbucket.com/repos/exampleappthree', extra_info=None,
                               production_pods=3, server='ab0003'))
    db.session.add(Application(name='Example App Four', team_name='Team Four',
                               team_email='team.four@gmail.com', url='https://exampleappfour.com',
                               swagger='https://exampleappfour.com/swagger/ui',
                               bitbucket='https://bitbucket.com/repos/exampleappfour', extra_info=None,
                               production_pods=2, server='ab0004'))
    db.session.add(Application(name='Example App Five', team_name='Team Five',
                               team_email='team.five@gmail.com', url='https://exampleappone.com',
                               swagger='https://exampleappfive.com/swagger/ui',
                               bitbucket='https://bitbucket.com/repos/exampleappfive', extra_info=None,
                               production_pods=1, server='ab0001'))
    db.session.add(Application(name='Example App Six', team_name='Team Six',
                               team_email='team.six@gmail.com', url='https://exampleappsix.com',
                               swagger='https://exampleappone.com/swagger/ui',
                               bitbucket='https://bitbucket.com/repos/exampleappsix', extra_info=None,
                               production_pods=3, server='ab0009'))
    db.session.add(Application(name='Example App Seven', team_name='Team Seven',
                               team_email='team.seven@gmail.com', url='https://exampleappseven.com',
                               swagger=None,
                               bitbucket='https://bitbucket.com/repos/exampleappseven', extra_info='This is an Angular application which uses Ngrx for state management',
                               production_pods=1, server='ab0010'))
    db.session.add(Application(name='Example App Eight', team_name='Team Eight',
                               team_email='team.eight@gmail.com', url='https://exampleappeight.com',
                               swagger='https://exampleappeight.com/swagger/ui',
                               bitbucket='https://bitbucket.com/repos/exampleappeight', extra_info=None,
                               production_pods=1, server='ab005'))
    db.session.add(Application(name='Example App Nine', team_name='Team Nine',
                               team_email='team.nine@gmail.com', url='https://exampleappnine.com',
                               swagger=None,
                               bitbucket='https://bitbucket.com/repos/exampleappnine', extra_info='This is a React application that is used to manage loans',
                               production_pods=2, server='ab0007'))
    db.session.add(Application(name='Example App Ten', team_name='Team Ten',
                               team_email='team.ten@gmail.com', url='https://exampleappten.com',
                               swagger='https://exampleappten.com/swagger/ui',
                               bitbucket='https://bitbucket.com/repos/exampleappten', extra_info=None,
                               production_pods=1, server='ab0002'))
    db.session.commit()