from flask import Blueprint, Response, current_app, redirect, render_template, url_for
from flask_login import login_required


api_blueprint = Blueprint('api_blueprint', __name__)

@api_blueprint.before_request
@login_required
def require_login():
    pass


@api_blueprint.route('/video_feed')
def video_feed():
    return Response(current_app.pi_guardian.generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@api_blueprint.route('/pic')
def take_picture():
    current_app.pi_guardian.take_picture()
    return redirect(url_for('views_blueprint.profiles'))
