from flask import Flask, render_template,flash,redirect,jsonify,session,url_for,g
from flask.globals import request
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
# source venv/bin/activate

from config import client,secret
app = Flask(__name__)
app.config['SECRET_KEY'] = secret
app.config['TEMPLATES_AUTO_RELOAD'] = True
# 22
#Database
db = client.asiriusweb
users = db.users

personID = ""
def people(email,password):
     id = ObjectId()
     return {
            "email": email,
            "password": password,
            "_id" : str(id)
        }
     
@app.route("/",methods = ['POST','GET'])
def dull():
    if request.method == "POST":
       email = request.form.get("email")
       password = request.form.get("password")
       email_found = users.find_one({"email": email})
       if email_found:
          email_val = email_found['email']
          passwordcheck = email_found['password']
            
          if pbkdf2_sha256.verify(password,passwordcheck):
             session["logged_in"] = True
             session["email"] = email
             print("here")
            #  return redirect(url_for("home"))
          else:
              print("wrongpass")
              message = 'Wrong password'
            #   return redirect(url_for("home"))
       else:
          print("notemail")
        #   return redirects(url_for("home"))   
    return render_template("dull.html")
@app.route("/home",methods = ['POST','GET'])
def home():
    # if 'email' in session:
    #    setUpHome()
    if request.method == "POST":
       email = request.form.get("email")
       password = request.form.get("password")
       email_found = users.find_one({"email": email})
       if email_found:
          email_val = email_found['email']
          passwordcheck = email_found['password']
            
          if pbkdf2_sha256.verify(password,passwordcheck):
             session["logged_in"] = True
             session["email"] = email
             print("here")
             star = 'lightStarIcon.svg'
            #  return redirect(url_for("home"))  
          else:
              print("wrongpass")
              message = 'Wrong password'
              return render_template('home.html', message=message)
       else:
          message = 'Email not found'
          print("notemail")
          return render_template('home.html', person=email)   
    return render_template('home.html')



@app.route("/create",methods = ['POST','GET'])
def create():
    if request.method == "POST":
        username = request.form.get("username")
        email = username+"@asirius.co"
        password = request.form.get("password")
        email_found = users.find_one({"email": email})
        if email_found:
          print("Email Already In Use','sorry")
          flash('Email Already In Use','sorry')
        else:
          encrypted_Password = pbkdf2_sha256.hash(password)
          users.insert_one(people(email,encrypted_Password))
          session["logged_in"] = True
          session["email"] = email
          print("You are successfully logged in")
          flash('You are successfully logged in','success')
          star = 'lightStarIcon.svg'
          return redirect(url_for("home", star_icon=star, person=username))
    return render_template('create.html')

@app.route("/subscribe")
def subscribe():
    return render_template('subscribe.html')

@app.route("/peeple")
def peeple():
    return redirect('https://apps.apple.com/ae/app/peeple-a-social-app/id1531359236')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/info")
def info():
    return render_template('info.html')

@app.route("/peeple/privacyPolicy")
def privacy_Policy():
    return render_template('PPP.html')

@app.route("/peeple/EULA")
def peeple_EULA():
    return render_template('PEULA.html')

@app.route("/peeple/support")
def peeple_Support():
    return render_template('support.html')

@app.route("/news")
def news():
    return render_template('news.html')

NewsPost = {
    'DateandTime' : "",
    'MessageText' : "",
    'MessageImage' : "",
    'ImageLink' : ""
}

Products = {
    'ProductImage' : "",
    'ProductAweCoin' : "",
    'ProductDescription' : ""
}

@app.route("/shop")
def shop():
    return render_template('shop.html')


if __name__ == '__main__':
    app.run()
