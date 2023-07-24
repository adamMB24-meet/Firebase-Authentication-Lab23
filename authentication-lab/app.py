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
  "databaseURL": "https://cs-firebase-y2-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#_________________________________________________________________________________________________________________________________________________________
@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('add_tweet'))
      #  except:
            #error = "Authentication failed"
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'GET':
       return render_template("signup.html")
    else:   
        email = request.form['email']
        password = request.form['password']
        #try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        UID = login_session['user']['localId']
        user = {"full_name": "Adam Meisler", "email": "a@gmail.com","username": "adamrmb07","bio": "Hi my name is adam, Im a Y2 student in MEET..."}
        db.child("Users").child(UID).set(user)
        return redirect(url_for('add_tweet'))
        #except:
            #error = "Authentication failed"
            #return render_template("signup.html", error=error)

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        #try:
        UID = login_session['user']['localId']
        tweet = {"title": request.form['title'], "tweet": request.form['tweet']}
        db.child("Tweet").push(tweet)
        return render_template("add_tweet.html")
        #except:
            #print("Couldn't add tweet")
           # return redirect(url_for('add_tweet'))
    #return render_template("add_tweet.html")

@app.route('/all_tweets', methods=['GET'])
def all_tweets():
    try:
        UID = login_session['user']['localId']
        all_tweets = db.child("Users").child(UID).child("Tweet").get().val()
        return render_template("all_tweets.html", all_tweets=all_tweets)
    except:
        error = "Process Failed"
        return render_template("error.html", error=error)

#_________________________________________________________________________________________________________________________________________________
if __name__ == '__main__':
    app.run(debug=True)