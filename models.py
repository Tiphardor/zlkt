# encoding:utf-8

from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telphone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Question(db.Model):
    __tablename__ = 'question'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # now()获取的是服务器第一次运行时间
    # now就是每次创建一个模型的时候，都获取当前的时间
    createTime = db.Column(db.DateTime, default=datetime.now)
    authorId = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('questions'))


class Answer(db.Model):
    __tablename__ = 'answer'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    createTime = db.Column(db.DateTime, default=datetime.now)
    questionId = db.Column(db.Integer, db.ForeignKey('question.id'))
    authorId = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.relationship('Question', backref=db.backref('answers', order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('answers'))
