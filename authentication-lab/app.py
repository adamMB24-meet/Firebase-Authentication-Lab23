from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyBgYZ3voLU1FNbM8J05bUvTFnbHyx7zMrs",
  "authDomain": "cs-firebase-y2.firebaseapp.com",
  "projectId": "cs-firebase-y2",
  "storageBucket": "cs-firebase-y2.appspot.com",
  "messagingSenderId": "996495197683",
 " appId": "1:996495197683:web:b77b737703ed5cce637e86",
  "measurementId": "G-91TMB3J5QK",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
         login_session['user'] = auth.sign_in_user_with_email_and_password(email,password)
         return redirect(url_for('add_tweet.html'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
        login_session['user'] = auth.create._user_with_email_and_password(email,password)
        return render_template("add_tweet.html")
       except:
           error = "Authentication failed"
   return render_template("signup.html")

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)