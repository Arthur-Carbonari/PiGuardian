import os
import re
from time import sleep
import unicodedata
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename


from flask_server.forms import NewProfileForm

views_blueprint = Blueprint('views_blueprint', __name__)

@views_blueprint.before_request
@login_required
def require_login():
    pass

@views_blueprint.route('/')
def home():
    return render_template('home.html')

@views_blueprint.route('/profiles', methods=['GET', 'POST'])
def profiles():

    profiles = current_app.get_profiles()

    new_profile_form: NewProfileForm = NewProfileForm()

    if new_profile_form.validate_on_submit():

        files = []

        for file_obj in list(request.files.listvalues())[0]:

            filename = secure_filename(file_obj.filename)
            # Access file data
            file_data = file_obj.read()  # Read file content

            files.append([filename, file_data])

        folder_name = new_profile_form.name.data

        current_app.add_profile(folder_name, files)

        # flash('Profile Created')
        sleep(3)
        return render_template('profiles.html', profiles=profiles, new_profile_form=new_profile_form)


    return render_template('profiles.html', profiles=profiles, new_profile_form=new_profile_form)
