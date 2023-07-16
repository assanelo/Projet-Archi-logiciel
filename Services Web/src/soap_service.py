from spyne import rpc, ServiceBase, Integer, Unicode
from werkzeug.security import generate_password_hash, check_password_hash

from zeep import Client
from zeep.wsse.username import UsernameToken

from models import User
from database import db

from flask import request
import jwt

SECRET_KEY = "DarouSalame"

def requires_auth(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if "admin" in payload:
                return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            pass
        except jwt.InvalidTokenError:
            pass
        return "Unauthorized", 401
    return decorated

# SOAP API service
class UserService(ServiceBase):
    @requires_auth
    @rpc(Integer, _returns=Unicode)
    def get_user(ctx, user_id):
        user = User.query.get(user_id)
        if user:
            return f"{{'id': {user.id}, 'pseudo': '{user.pseudo}', 'email': '{user.email}', 'profil': '{user.profil}'}}"
        return None
    @requires_auth
    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=bool)
    def add_user(ctx, pseudo, password, email, profil):
        # Check if the user already exists with the same pseudo or email
        if User.query.filter_by(pseudo=pseudo).first() or User.query.filter_by(email=email).first():
            return False  # User already exists, cannot add again

        # Generate a hash of the user's password
        hashed_password = generate_password_hash(password)

        # Create a new user object and add it to the database
        new_user = User(pseudo=pseudo, password=hashed_password, email=email, profil=profil)
        db.session.add(new_user)
        db.session.commit()

        return True  # User added successfully

    @requires_auth
    @rpc(Integer, Unicode, Unicode, Unicode, Unicode, _returns=bool)
    def update_user(ctx, user_id, pseudo, password, email, profil):
        # Find the user with the provided user_id in the database
        user = User.query.get(user_id)
        if not user:
            return False  # User with the given user_id not found

        # Check if the new pseudo or email is already taken by another user
        existing_user_by_pseudo = User.query.filter_by(pseudo=pseudo).first()
        existing_user_by_email = User.query.filter_by(email=email).first()
        if (existing_user_by_pseudo and existing_user_by_pseudo.id != user_id) or (existing_user_by_email and existing_user_by_email.id != user_id):
            return False  # New pseudo or email is already taken by another user

        # Update the user's data
        user.pseudo = pseudo
        if password:
            hashed_password = generate_password_hash(password)
            user.password = hashed_password
        user.email = email
        user.profil = profil

        # Commit the changes to the database
        db.session.commit()

        return True  # User updated successfully update

    @requires_auth
    @rpc(Integer, _returns=bool)
    def delete_user(ctx, user_id):
        # Find the user with the provided user_id in the database
        user = User.query.get(user_id)
        if not user:
            return False  # User with the given user_id not found

        try:
            # Delete the user from the database
            db.session.delete(user)
            db.session.commit()
            return True  # User deleted successfully
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            db.session.rollback()
            return False  # Failed to delete user
    
    @requires_auth
    @rpc(Unicode, Unicode, _returns=Unicode)
    def generer_token(ctx, username, password):
        # Vérifiez les informations d'identification de l'administrateur
        if username == "admin" and password == "mot_de_passe_admin":
            # Générez le jeton d'authentification avec une durée de validité (par exemple, 1 heure)
            token_payload = {"admin": True}
            token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")
            return token
        return "Unauthorized"

    
    @rpc(Unicode, Unicode, _returns=bool)
    def authentifier_utilisateur(ctx, login, password):
        user = User.query.filter_by(pseudo=login).first()
        if user and check_password_hash(user.password, password):
            return True
        return False
    



