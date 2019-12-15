from flask import Blueprint, render_template, request, flash
from flask import abort, url_for, redirect
from functools import wraps
from flask_login import login_user, logout_user, login_required, current_user
from .verification import RegisterationForm, LoginForm
from ..user.model import User, Identity
from ... import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def manager_required(permission):
    def decorator(func):           
        @wraps(func)               
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            print(current_user)
            user_permission = current_user.identity
            if user_permission and user_permission == permission:
                return func(*args, **kwargs)
            else:                  
                abort(403)         
        return decorated_function
    return decorator


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        id = request.form['id']
        user = User.query.filter_by(id=id).first()
        password_input = request.form['password']
        password_db = user.password
        if user and password_input == password_db:
            login_user(user)
            flash('欢迎回来.', category='success')
            return redirect(url_for('index'))
        else:
            flash('用户名不存在或密码错误.', category='danger')
            return redirect(url_for('auth.login'))
    return render_template('auth/auth.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
@manager_required(3)
def register():
    form = RegisterationForm(request.form)
    if request.method == "POST" and form.validate():
        id = request.form['id']
        user = User.query.filter_by(id=id).first()
        if user:
            flash('用户已存在.', category="warning")
            return redirect(url_for('auth.register'))
        else:
            username = request.form['username']
            password = request.form['password']
            phone = request.form['phone']
            type = request.form['type']
            identity = Identity.query.filter_by(type=type).first()
            user = User(
                id=id,
                username=username,
                password=password,
                phone=phone,
                identity=identity.id
            )
            db.session.add(user)
            flash('恭喜你注册成功.', category="success")
            return redirect(url_for('auth.login'))
    return render_template('auth/auth.html', form=form)


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('用户退出成功', 'success')
    return redirect(url_for('index'))
