from flask import Flask, render_template, url_for
app = Flask(__name__)


posts=[
	{
	'autor':'Andre Santos', 
	'title':'Publicação de teste Web App', 
	'content':'Primeiro conteúdo publicado', 
	'date_posted':'7 de julho de 2019'
	},
	{
	'autor':'Gustavo Barros', 
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


if __name__ == '__main__':
	app.run(debug=True)