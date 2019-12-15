from wtforms import StringField, PasswordField, validators, Form


class LoginForm(Form):
    id = StringField('id', [
        validators.Length(8, message="学号格式不正确"),
        validators.DataRequired('请输入学号')
    ])
    password = PasswordField('password', [
        validators.DataRequired('请输入密码')
    ])


class RegisterationForm(Form):
    id = StringField('id', [
        validators.Length(8, message="学号格式不正确"),
        validators.DataRequired('请输入学号')
    ])
    username = StringField('username', [
        validators.Length(min=2, max=10, message="用户名长度不规范")
    ])
    phone = StringField('phone', [
        validators.DataRequired('请输入手机'),
        validators.Length(11, message="手机格式不正确")
    ])
    password = PasswordField('password', [
        validators.DataRequired('请输入密码'),
        validators.EqualTo('confirm', message='密码不匹配')
    ])
    confirm = PasswordField('confirm', [
        validators.DataRequired('请再次输入密码')
    ])
