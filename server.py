from flask import Flask, render_template, redirect, request, flash, session, jsonify
from mysqlconnection import connectToMySQL       
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__) 
app.secret_key = 'keep it secret, keep it safe'

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/email_check", methods=["POST"])
def email_check():
    found = False
    if not EMAIL_REGEX.match(request.form["email"]):
        return jsonify(message = "Email has incorrect format!!", status= False)
    query = "SELECT email FROM emails WHERE email = %(email)s;"
    data = {
        'email': request.form['email']
    }
    results = connectToMySQL('ajaxEmail').query_db(query,data)
    if results:
        found = True
        return render_template("/partials/email_check.html", found=found)
    return jsonify(message = "Email is available", status= True)


@app.route('/create_email', methods=['POST'])
def create_user():
    query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW())"
    data = {
        'email': request.form['email']
    }
    results = connectToMySQL("ajaxEmail").query_db(query, data)
    print("############",results)
    session['id'] = results
    return redirect("/")


@app.route('/success')
def success():
    if 'id' not in session:
        return redirect("/")
    query = "SELECT * FROM emails WHERE id = %(id)s;"
    data = {
        "id": session['id'],
    }
    mysql = connectToMySQL('ajaxEmail')
    result = mysql.query_db(query,data)[0]
    print(result)
    return render_template("success.html", email = result)

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

if __name__=='__main__':
    app.run(debug=True)