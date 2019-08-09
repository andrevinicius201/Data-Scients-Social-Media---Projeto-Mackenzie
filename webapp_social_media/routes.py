from flask import render_template, url_for, flash, redirect
from webapp_social_media import app
from webapp_social_media.forms import RegistrationForm, LoginForm
from webapp_social_media.models import User, Post

posts=[
	{
	'author':'Andre Santos', 
	'title':'Publicação de teste Web App', 
	'content':'Primeiro conteúdo publicado', 
	'date_posted':'7 de julho de 2019'
	},
	{
	'author':'Gustavo Barros', 
	'title':'Criando aplicações para Web', 
	'content':'Segundo conteúdo publicado', 
	'date_posted':'08 de agosto de 2019'
	},
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You have been logged in', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login unsuccessfull. Please check your username and password', 'danger')
	return render_template('login.html', title='Login', form=form)
