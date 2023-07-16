from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from database import db

# User model for Flask-Login
class UserModel(UserMixin):
    pass

# Flask-WTF forms
class ArticleForm(FlaskForm):
    titre = StringField('Titre', validators=[DataRequired(), Length(max=255)])
    contenu = TextAreaField('Contenu', validators=[DataRequired()])
    categorie = SelectField('Catégorie', coerce=int, validators=[DataRequired()])

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255))
    contenu = db.Column(db.Text)
    dateCreation = db.Column(db.DateTime, default=db.func.current_timestamp())
    dateModification = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    categorie = db.Column(db.Integer, db.ForeignKey('categorie.id'))

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(20))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    profil = db.Column(db.String(100), nullable=False)

