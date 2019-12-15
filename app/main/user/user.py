from flask import render_template, request, jsonify
from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from .verification import ModificationForm
from .model import Identity
from ..book.model import Borrow
from ... import db
import requests
import json

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
@login_required
def show():
    user = current_user
    identity = Identity.query.filter_by(id=user.identity).first()
    borrows = Borrow.query.filter_by(user_id=current_user.id).all()
    user = user.to_json()
    identity = identity.to_json()
    return render_template(
        'user/show_user.html',
        user=user,
        identity=identity,
        borrows=borrows
    )


@bp.route('/modify', methods=['GET', 'POST'])
@login_required
def modify():
    user = current_user
    form = ModificationForm(request.form)
    if request.method == "POST" and form.validate():
        user = current_user
        user.phone = request.form['phone']
        user.password = request.form['password']
        db.session.add(user)
        flash('修改成功', 'success')
        return redirect(url_for('user.show'))
    return render_template('user/modify_user.html', user=user, form=form)


url_base = "https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province={}&city={}"


def get_weather(province, city):
    url = url_base.format(province, city)
    response = requests.get(url)
    content = response.content
    content_json = json.loads(content)
    data = content_json.get('data')
    observe = data.get('observe')
    tips = data.get('tips')
    return observe, tips


@bp.route('/weather')
def weather():
    province = request.args.get('province', type=str)
    city = request.args.get('city', type=str)
    observe, tips = get_weather(province, city)
    return jsonify(observe, tips)
