from flask import Flask, redirect, url_for, session, request, render_template
from requests_oauthlib import OAuth2Session

import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# Configuración de OAuth
CLIENT_ID = "aqui la cadena de caracteres que te da google"
CLIENT_SECRET = "AQUI LA CADENA DE CARACTERES QUE TE DA GOOGLE"
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REDIRECT_URI = "http://localhost:5000/callback"
SCOPE = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]

app = Flask(__name__)
app.secret_key = "clave_secreta_segura_12345"  # Asegurar una clave secreta fuerte

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = google.authorization_url(AUTHORIZATION_BASE_URL)
    session["oauth_state"] = state  # Guardar el estado en la sesión
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    if "oauth_state" not in session:  # Verificar que oauth_state exista antes de usarlo
        return redirect(url_for("index"))

    google = OAuth2Session(CLIENT_ID, state=session["oauth_state"], redirect_uri=REDIRECT_URI)
    token = google.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)
    session["oauth_token"] = token
    return redirect(url_for("profile"))

@app.route("/profile")
def profile():
    if "oauth_token" not in session:
        return redirect(url_for("index"))

    google = OAuth2Session(CLIENT_ID, token=session["oauth_token"])
    user_info = google.get("https://www.googleapis.com/oauth2/v1/userinfo?alt=json").json()

    return render_template("profile.html", user=user_info)
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
