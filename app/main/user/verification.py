from wtforms import StringField, PasswordField,  validators, Form


class ModificationForm(Form):
    phone = StringField('phone', [
        validators.Length(11, message="联系方式错误")
    ])
    password = PasswordField('password', [
        validators.DataRequired('请输入密码'),
        validators.EqualTo('confirm', message='密码不匹配')
    ])
    confirm = PasswordField('confirm', [
        validators.DataRequired('请再次输入密码')
    ])
