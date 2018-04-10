
from flask import Flask, request, redirect,render_template
import cgi
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/signup')
def display_signup_form():
    template = jinja_env.get_template('signupform.html')
    return template.render()

def isValidEmail(email):
    if len(email) > 7 :
        if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
            return True
    else:
        return False


def is_empty(text):
    try:
        if text !='':
            return True
    except ValueError:
        return False

        

@app.route('/signup', methods=['POST'])
def validate_form():

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password2=request.form['password2']

    username_error = ''
    email_error = ''
    password_error=''
    password_error2=''

    if not is_empty(username):
        username_error = 'Error empty username'
        username = ''
    else:
        username_length = len(username)
        if username_length < 3 or username_length>20:
            username_error = 'Wrong username length'
            username = ''

    if not is_empty(email):
        email_error = 'Field is empty'
        email = ''
    else:
        if isValidEmail(email) == False:
            email_error = 'This is not a valid email'
            email = ''
    if not is_empty(password):
        password_error='This field is empty'
        password=''
    else:
        password_length=len(password)
        if password_length<3 or password_length>20:
            password_error="There's been an error in your password"
            password =''
    if password != password2:
        password_error2="Does not match"

    if not username_error and not email_error and not password_error:
        username_welcome = username
        return redirect('/valid-form?username_welcome={0}'.format(username_welcome))
    else:
        template = jinja_env.get_template('signupform.html')
        return template.render(username_error=username_error,
            email_error=email_error,password_error=password_error,
            password_error2=password_error2,
            username=username, email=email, password=password,
            password2=password2)


@app.route('/valid-form')
def valid_form():
    username_welcome = request.args.get('username_welcome')
    return '<h1>You submitted {0}. Thanks for submitting a valid time!</h1>'.format(username_welcome)





app.run()