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
        """

    application_id: int = db.Column(db.Integer, primary_key = True)
    name: str = db.Column(db.String(150), unique = True)
    owner_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_name: str = db.Column(db.String(150))
    team_email: str = db.Column(db.String(150))
    url: str = db.Column(db.String(150))
    swagger: str = db.Column(db.String(150))
    bitbucket: str = db.Column(db.String(200), unique = True)
    extra_info: str = db.Column(db.Text(200))
    production_pods: str = db.Column(db.Integer)
    created: datetime.datetime= db.Column(db.DateTime, default=datetime.datetime.now())