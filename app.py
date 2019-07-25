# encoding:utf-8
from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Question, Answer
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by(Question.createTime.desc()).all()
    }
    return render_template('index.html', **context)


@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    answer_content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content=answer_content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question_model = Question.query.filter(Question.id == question_id).first()
    answer.question = question_model
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telphone = request.form.get('telphone')
        password = request.form.get('password')
        user = User.query.filter(User.telphone == telphone, User.password ==
                                 password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或密码不正确，请核对后重试！'


@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # def session['user_id']
    session.clear()
    return redirect(url_for('login'))


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telphone = request.form.get('telphone')
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        user = User.query.filter(User.telphone == telphone).first()
        if user:
            return u'该手机号码已被注册，请更换手机号码后重试！'
        else:
            if password != repassword:
                return u'两次密码输入不同，请核对后重试！'
            else:
                user = User(telphone=telphone, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.context_processor
def context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
