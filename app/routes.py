from flask import render_template, flash, redirect
from flask import request, url_for
from werkzeug.urls import url_parse
from flask_login import current_user, login_user
from flask_login import logout_user, login_required
from app import app
from app import db
from app.models import User
from app.forms import LoginForm
from app.forms import WeighingForm
from app.models import Weighing
import datetime

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    weighings = Weighing.query.order_by(Weighing.weighing_time.desc()).paginate(
        page, app.config['WEIGHINGS_PER_PAGE'], False)
    next_url = url_for('index', page=weighings.next_num) \
        if weighings.has_next else None
    prev_url = url_for('index', page=weighings.prev_num) \
        if weighings.has_prev else None
    return render_template("index.html", title='Home', weighings=weighings.items,
                          next_url=next_url, prev_url=prev_url)

@app.route('/explore', methods=['GET', 'POST'])
#@login_required
def explore():
    form = WeighingForm()
    if form.validate_on_submit():
        weighing = Weighing(weight=form.weight.data,
        geolocation=form.geolocation.data,
        weighing_time=form.weighing_time.data,
        author=current_user)
        db.session.add(weighing)
        db.session.commit()
        flash('Weighing successfully saved.')
        return redirect(url_for('explore'))
    page = request.args.get('page', 1, type=int)
    weighings = Weighing.query.paginate(
        page, app.config['WEIGHINGS_PER_PAGE'], False)
    next_url = url_for('explore', page=weighings.next_num) \
        if weighings.has_next else None
    prev_url = url_for('explore', page=weighings.prev_num) \
        if weighings.has_prev else None
    return render_template('index.html', title='Register Weighing', form=form,
                           weighings=weighings.items, next_url=next_url,
                           prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.index'))