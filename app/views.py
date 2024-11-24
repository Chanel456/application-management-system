from flask import render_template, Blueprint
from flask_login import login_required, current_user

from app import db
from app.application.forms import ApplicationForm
from app.models.application import Application
from app.models.server import Server

views = Blueprint('views', __name__)

@views.route('/dashboard')
@login_required
def dashboard():
    form = ApplicationForm()
    applications = db.session.query(Application).all()
    return render_template('application/grid.html', user=current_user, form=form, list=applications)

@views.route('/servers')
@login_required
def grid():
    servers = db.session.query(Server).all()
    return render_template('server/grid.html', user=current_user, list=servers)