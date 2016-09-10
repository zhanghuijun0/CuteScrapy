# coding:utf8
from flask import Flask,request,render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

from CuteScrapy.model.blogs import Blogs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zhanghuijun'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(Form):
    name = StringField(u'你的名字？',validators=[Required()])
    submit = SubmitField(u'提交')



@app.route('/',methods=['post','get'])
def index():
    return render_template('index.html',current_time=datetime.utcnow())


@app.route('/home',methods=['post','get'])
def home():
    blogs = Blogs()
    data = blogs.getAll()
    return render_template('list.html',data = data)

@app.route('/page.html',methods=['post','get'])
def signin_form():
    name = None
    nameForm = NameForm()

    if nameForm.validate_on_submit():
        name = nameForm.name.data
        nameForm.name.data = ''

    return render_template('page.html',form=nameForm,name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/signin',methods=['post'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'pwd':
        return render_template('signin-ok.html',username = username)
    return  render_template('error.html',message='Error pwd',username = username)

if __name__ == '__main__':
    app.run()