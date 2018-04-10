from flask import Flask, request, redirect, render_template
import re
import os

app = Flask(__name__)
app.config['DEBUG'] == True

@app.route("/")
def index():
    '''alternative with autoescparing to initiliazing a template
    then doing .render().'''
    return render_template('index.html')

def does_pw_match(password, verify):
    return password == verify

def is_email_valid(email):
    # re.match doesn't normally return a boolean hence is not None at end
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is not None

def is_username_valid(username):
    '''^...$ is important for only matching if the whole
    string is exactly what you want'''
    return re.match(r'^[\S]{3,20}$', username) is not None


@app.route("/", methods=['POST'])
def validate():
    # variables need to be taken from form
    username = request.form["username"]
    password = request.form["password"]
    verify = request.form["verify"]
    email = request.form["email"]
    # errors should be blank as default
    username_error = ""
    password_error = ""
    email_error = ""

    #Conditionals for when username, password, etc. is not valid
    if not is_username_valid(username):
        username_error = "Invalid Username"
        username = ""
    if not does_pw_match(password, verify):
        password_error = "Passwords didn't match"
        password = ""
        verify = ""
    if not email:
        pass    
    elif not is_email_valid(email):
            email_error = "Invalid Email Address"
            email = ""
    #Code runs if there are no errors.
    if not username_error and not password_error and not email_error:
        return render_template("welcome.html", username = username)
    else: #runs if there are errors
        return render_template('index.html', username_error=username_error,
            password_error=password_error, email_error= email_error,
            username = username, password = password, email = email,
            verify = verify)
    



app.run()