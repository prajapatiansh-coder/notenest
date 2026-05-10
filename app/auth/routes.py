import os
import secrets
from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from ..extensions import db
from ..models.user import User
from ..models.note import Note
from ..models.interaction import Notification
from .forms import RegistrationForm, LoginForm, UpdateProfileForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('notes.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('notes.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('notes.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('notes.index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['PROFILE_PICS'], picture_fn)
    
    # Save the file
    form_picture.save(picture_path)
    
    return picture_fn

@auth_bp.route("/profile/<string:username>", methods=['GET', 'POST'])
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    user_notes = Note.query.filter_by(user_id=user.id).order_by(Note.uploaded_at.desc()).all()
    total_downloads = sum(note.downloads for note in user_notes)
    
    form = None
    if current_user.is_authenticated and current_user.id == user.id:
        form = UpdateProfileForm(current_user.username, current_user.email)
        if form.validate_on_submit():
            if form.picture.data:
                # Delete old avatar if not default
                if current_user.avatar != 'default.jpg':
                    old_path = os.path.join(current_app.config['PROFILE_PICS'], current_user.avatar)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                picture_file = save_picture(form.picture.data)
                current_user.avatar = picture_file
            
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('auth.profile', username=current_user.username))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
            
    return render_template('auth/profile.html', user=user, notes=user_notes, total_downloads=total_downloads, form=form)

@auth_bp.route("/notifications")
@login_required
def notifications():
    notes = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('auth/notifications.html', title='Notifications', notifications=notes)

@auth_bp.route("/notifications/read/<int:notif_id>")
@login_required
def mark_read(notif_id):
    notification = Notification.query.get_or_404(notif_id)
    if notification.user != current_user:
        abort(403)
    notification.is_read = True
    db.session.commit()
    if notification.link:
        return redirect(notification.link)
    return redirect(url_for('auth.notifications'))

@auth_bp.route("/notifications/clear")
@login_required
def clear_notifications():
    Notification.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Notifications cleared.', 'info')
    return redirect(url_for('auth.notifications'))
