from flask import Flask
from database import db

from flask import Flask, request, jsonify
from flask_restful import Api

from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from restful_resources import AllArticlesResource, ArticlesByCategoryResource, ArticleResource, UserResource
from soap_service import UserService
from database import db

from flask_migrate import Migrate


app = Flask(__name__)

app.config['SECRET_KEY'] = 'DarouSalame'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:okok@localhost/mglsi_news'

# Initialize the database with the app
db.init_app(app)
migrate = Migrate(app, db)


api = Api(app)

api.add_resource(UserResource, '/api/users')
api.add_resource(AllArticlesResource, '/api/articles')
api.add_resource(ArticlesByCategoryResource, '/api/categories/<int:category_id>/articles')
api.add_resource(ArticleResource, '/api/article/<int:article_id>')

soap_app = Application([UserService], 'UserService', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
soap_service = WsgiApplication(soap_app)

# Add SOAP API service to the Spyne application
soap_app = Application([UserService], 'UserService',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

@app.route('/soap/add_user', methods=['POST'])
def add_user_soap():
    data = request.get_json()
    pseudo = data.get('pseudo')
    password = data.get('password')
    email = data.get('email')
    profil = data.get('profil')

    # Call the add_user function from soap_service
    result = UserService.add_user(soap_service, pseudo, password, email, profil)

    if result:
        return jsonify({"message": "Utilisateur ajouté avec succès."}), 201
    else:
        return jsonify({"message": "Impossible d'ajouter l'utilisateur. Vérifiez les données saisies."}), 400


# Route to update a user using SOAP service
@app.route('/soap/get_user', methods=['GET'])
def get_user_soap():
    data = request.get_json()
    user_id = data.get('user_id')

    # Call the get_user SOAP method from the UserService with ctx argument
    result = UserService.get_user(user_id, ctx=soap_service)

    if result:
        return result, 200
    else:
        return jsonify({"message": "Utilisateur introuvable. Vérifiez l'ID de l'utilisateur."}), 404



@app.route('/soap/update_user', methods=['POST'])
def update_user_soap():
    data = request.get_json()
    user_id = data.get('user_id')
    pseudo = data.get('pseudo')
    password = data.get('password')
    email = data.get('email')
    profil = data.get('profil')

    # Call the update_user SOAP method from the UserService with ctx argument
    result = UserService.update_user(user_id, pseudo, password, email, profil, ctx=soap_service)

    if result:
        return jsonify({"message": "Utilisateur mis à jour avec succès."}), 200
    else:
        return jsonify({"message": "Impossible de mettre à jour l'utilisateur. Vérifiez les données saisies."}), 400


@app.route('/soap/delete_user', methods=['POST'])
def delete_user_soap():
    data = request.get_json()
    user_id = data.get('user_id')

    # Call the delete_user SOAP method from the UserService with ctx argument
    result = UserService.delete_user(user_id, ctx=soap_service)

    if result:
        return jsonify({"message": "Utilisateur supprimé avec succès."}), 200
    else:
        return jsonify({"message": "Impossible de supprimer l'utilisateur. Vérifiez l'ID de l'utilisateur."}), 400


# Définir une route pour le service SOAP
@app.route('/soap/auth', methods=['POST'])
def auth():
    if request.method == 'POST':
        login = request.json.get('login')
        password = request.json.get('password')
        result = UserService.authentifier_utilisateur(soap_service, login, password)
        if result:
            return jsonify({"message": "Utilisateur connecté avec succès.",}), 200
        else:
            return jsonify({"message": "Impossible de connecté l'utilisateur. Vérifiez l'ID de l'utilisateur."}), 400

if __name__ == '__main__':
    app.run(debug=True)

    
