from flask import Flask, render_template, jsonify
import requests
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from models import Article

app = Flask(__name__)

@app.route('/')
def index():
    # Récupérer tous les articles à partir de l'API
    # pour afficher la liste des derniers articles avec une description sommaire
    response = requests.get('http://localhost:5000/api/articles')
    if response.status_code == 200:
        data = response.json()
        # Création d'une liste pour stocker les objets Article
        articles = []

        # Boucle pour créer les objets Article et les ajouter à la liste
        for article_data in data["articles"]:
            article = Article(article_data["id"], article_data["titre"], article_data["contenu"])
            articles.append(article)

        # Affichage des articles
        for article in articles:
            print(article)
    else:
        articles = []

    return render_template('index.html', articles=articles)

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    """ response = tuple(requests.get(f'http://localhost:5000/api/article/{article_id}'))
    article_ = None  # Initialisation avec une valeur par défaut

    if response.status_code == 200:
        data = response.json()
        # Création d'un objet Article à partir des données
        article_ = Article(data["id"], data["titre"], data["contenu"])
        print(article_)
    else:
        print('Pas d article')

    return render_template('article_detail.html', article=article_) """
    requests.get(f'http://localhost:5000/api/article/{article_id}')
    return 'some thing'
    
    

@app.route('/categorie/<int:category_id>')
def articles_by_category(category_id):
    # Récupérer les articles par catégorie à partir de l'API
    response = requests.get(f'http://localhost:5000/api/categories/{category_id}/articles')
    if response.status_code == 200:
        data = response.json()
        # Création d'une liste pour stocker les objets Article
        articles = []

        # Boucle pour créer les objets Article et les ajouter à la liste
        for article_data in data["articles"]:
            article = Article(article_data["id"], article_data["titre"], article_data["contenu"])
            articles.append(article)

        # Affichage des articles
        for article in articles:
            print(article)
    else:
        articles = []

    return render_template('articles_by_category.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
