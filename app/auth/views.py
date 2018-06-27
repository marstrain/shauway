from flask import render_template, redirect, request, url_for, flash, session, g
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .. import db
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ForgetPasswordForm, ResetPasswordForm
from ..email import send_email


@auth.route('/login', methods = ['GET', 'POST'])
def login():

    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Login Success!')
            next = request.args.get('next')
            '''if not is_safe_url(next):
                return abort(400)
            '''
            return redirect(next or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form )




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your Accout',
                   'auth/email/confirm', user=user, token=token)

        flash('Regist success, a confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.active:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your accout .Thanks!')
    else:
        flash('The link is invalid or has expired.')
    return redirect(url_for('main.index'))



@auth.before_app_request
def before_request():
    g.user = current_user
    if current_user.is_authenticated \
            and not current_user.active \
            and (request.endpoint != None and request.endpoint[:5]!='auth.')\
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.active:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm your accout',
               'auth/email/confirm', user=current_user, token = token)
    flash('A new confirmation has been sent to you by email.')
    return redirect(url_for('main.index'))

@auth.route('/change_password', methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.is_authenticated\
                and  current_user.verify_password(form.oldpassword.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Password changed,Please keep it!')
    else:
        flash('Changed faild, invalid password')
    return render_template('auth/change_password.html',form=form)


@auth.route('/reset_password', methods=['GET','POST'])
def reset_password_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html')






@auth.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been reset.')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',form=form)

@auth.route('/forget_password', methods=['GET','POST'])
def forget_password():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset your password',
               'auth/email/reset_password', user=user, token = token)
            flash('A email has been sent to you, please follow the instraction')
            return redirect(url_for('auth.login'))
    return render_template('auth/forget_password.html',form=form)

