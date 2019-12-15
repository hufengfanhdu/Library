from wtforms import StringField, IntegerField, FloatField, validators, Form


class AddBookForm(Form):
    name = StringField('name', [
        validators.DataRequired('请输入书名'),
    ])
    author = StringField('author', [
        validators.DataRequired('请输入作者'),
    ])
    publish = StringField('publish', [
        validators.DataRequired('请输入出版商'),
    ])
    amount = IntegerField('amount', [
        validators.DataRequired('请输入数量'),
    ])
    price = FloatField('price', [
        validators.DataRequired('请输入价格'),
    ])
    category = StringField('category', [
        validators.DataRequired('请输入分类'),
    ])
