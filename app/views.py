from flask import render_template, Blueprint
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)