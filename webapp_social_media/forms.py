from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from webapp_social_media.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Escolha um nome de usuário. Você pode alterar isso mais tarde!', 
		validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Endereço de E-mail', validators=[DataRequired(), Email()])
	password = PasswordField('Senha', validators=[DataRequired()])
	confirm_password = PasswordField('Confirme sua senha', validators=[DataRequired(), EqualTo('password')])
	data_nasc = StringField('Data de nascimento (dd/mm/aaaa)', 
		validators=[DataRequired(), Length(min=2, max=20)])
	start_work_date = StringField('Data de início de trabalho com ciência de dados (dd/mm/aaaa)', 
		validators=[DataRequired(), Length(min=2, max=20)])
	work_state = StringField('Estado onde você trabalha', 
		validators=[DataRequired(), Length(min=2, max=20)])
	work_city = StringField('Cidade onde você trabalha', 
		validators=[DataRequired(), Length(min=2, max=20)])
	salary = FloatField('Seu salário atual', 
		validators=[DataRequired()])
	instruction = StringField('Seu nível de instrução', 
		validators=[DataRequired()])
	company = StringField('Nome da empresa que você trabalha atualmente', 
		validators=[DataRequired()])
	submit = SubmitField('Criar conta')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()]) 
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username', 
		validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	data_nasc = StringField('Data de nascimento', validators=[DataRequired(), Length(min=2, max=20)])
	start_work_date = StringField('Data de início de trabalho com ciência de dados', validators=[DataRequired(), Length(min=2, max=20)])
	work_state = StringField('Estado onde você trabalha', validators=[DataRequired(), Length(min=2, max=20)])
	work_city = StringField('Cidade onde você trabalha', validators=[DataRequired(), Length(min=2, max=20)])
	salary = FloatField('Seu salário atual', validators=[DataRequired()])
	instruction = StringField('Seu nível de instrução', validators=[DataRequired(), Length(min=2, max=20)])
	company = StringField('Nome da empresa que você trabalha atualmente', validators=[DataRequired(), Length(min=2, max=40)])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')