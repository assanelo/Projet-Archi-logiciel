from flask_restful import Resource
from flask import request, jsonify, make_response
from models import Article, User
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from database import db


# RESTful API resources
class AllArticlesResource(Resource):
    def get(self):
        # Retrieve all articles from the database
        articles = Article.query.all()

        # Choose the response format (JSON or XML) based on the request's Accept header
        if 'application/xml' in request.headers.get('Accept'):
            # Return XML response
            response = {"articles": [{"id": article.id, "titre": article.titre, "contenu": article.contenu} for article in articles]}
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            # Return JSON response
            return jsonify(articles=[{"id": article.id, "titre": article.titre, "contenu": article.contenu} for article in articles])

class ArticlesByCategoryResource(Resource):
    def get(self, category_id):
        # Retrieve articles by category from the database
        articles = Article.query.filter_by(categorie=category_id).all()

        # Choose the response format (JSON or XML) based on the request's Accept header
        if 'application/xml' in request.headers.get('Accept'):
            # Return XML response
            response = {"articles": [{"id": article.id, "titre": article.titre, "contenu": article.contenu} for article in articles]}
            return response, 200, {'Content-Type': 'application/xml'}
        else:
            # Return JSON response
            return jsonify(articles=[{"id": article.id, "titre": article.titre, "contenu": article.contenu} for article in articles])

from flask import request, make_response, jsonify
from flask_restful import Resource

class ArticleResource(Resource):
    def get(self, article_id):
        # Retrieve the article from the database based on the given article_id
        article = Article.query.get(article_id)

        # Check if the article exists
        if not article:
            return {"message": "Article not found."}, 404

        # Choose the response format (JSON or XML) based on the request's Accept header
        if 'application/xml' in request.headers.get('Accept'):
            # Return XML response
            xml_response = f"<article><id>{article.id}</id><titre>{article.titre}</titre><contenu>{article.contenu}</contenu></article>"
            return make_response(xml_response, 200, {'Content-Type': 'application/xml'})
        else:
            # Return JSON response
            return jsonify(article={"id": article.id, "titre": article.titre, "contenu": article.contenu}), 200


# restful_resources.py
class UserResource(Resource):
    def post(self):
        # Parse the request data
        parser = reqparse.RequestParser()
        parser.add_argument('pseudo', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('profil', type=str, required=True)
        args = parser.parse_args()

        # Check if the user already exists with the same pseudo or email
        if User.query.filter_by(pseudo=args['pseudo']).first() or User.query.filter_by(email=args['email']).first():
            return {"message": "User already exists with the same pseudo or email."}, 409

        # Generate a hash of the user's password
        hashed_password = generate_password_hash(args['password'])

        # Create a new user object and add it to the database
        new_user = User(pseudo=args['pseudo'], password=hashed_password, email=args['email'], profil=args['profil'])
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User added successfully."}, 201
