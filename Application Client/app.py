from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = 'DarouSalame'

# Base URL du service web Flask
API_BASE_URL = 'http://localhost:5000'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        # Appel au service web pour authentifier l'utilisateur
        auth_data = {'login': login, 'password': password}
        response = requests.post(f"{API_BASE_URL}/soap/auth", json=auth_data)

        if response.status_code == 200 and response.json():
            # Authentification réussie, rediriger vers le dashboard
            return redirect('/dashboard')

        return render_template('login.html', error="Identifiants invalides.")
    
    return render_template('login.html')

@app.route('/', methods=['GET'])
def dashboard():
    if 'token' in session:
        token = session['token']

        # Appel au service web pour récupérer la liste des utilisateurs
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f"{API_BASE_URL}/soap/get_all_users", headers=headers)

        if response.status_code == 200:
            users = response.json()
            return render_template('dashboard.html', users=users)
        else:
            return render_template('dashboard.html', error="Impossible de récupérer la liste des utilisateurs.")
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

