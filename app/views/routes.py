from flask import render_template
from flask_login import login_required, current_user

from app.views import views

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('views/dashboard.html', user=current_user)