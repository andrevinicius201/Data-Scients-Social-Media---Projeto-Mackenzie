from PIL import Image
import secrets
import os
from flask import render_template, url_for, flash, redirect, request, abort
from webapp_social_media import app, db, bcrypt
from webapp_social_media.forms import RegistrationForm, RegistrationFormPremium, LoginForm, UpdateAccountForm, PostForm, UserInterestForm
from webapp_social_media.models import User, Post, InterestTopic, InterestTopicUser
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    return render_template('home.html', title='Home')


@app.route("/")
@app.route("/feed")
def feed():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=current_user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('feed.html', posts=posts)


@app.route('/interests/<string:username>', methods=['GET', 'POST'])
def user_interests(username):
    form = UserInterestForm()
    user = User.query.filter_by(username=username).first_or_404()     

    if request.method == 'POST':
        interests = request.form.getlist('interests')
        
        user_interest = InterestTopicUser.query.filter_by(user_id=user.id)

        for u in user_interest:
            db.session.delete(u)

        for i in interests:
            interest = InterestTopic.query.filter_by(label=i).first_or_404()
            userInterest = InterestTopicUser(topic=interest, interested=user)
            db.session.add(userInterest)

        db.session.commit()
        return redirect(url_for('home'))

    elif request.method == 'GET':        
        user_interest = InterestTopicUser.query.filter_by(interested=user)
        user_interest_list = []
        for u in user_interest:
            user_interest_list.append(u.topic_id)        
        interests = InterestTopic.query.all()
        image_file = url_for(
        'static', filename='profile_pics/' + user.image_file)
        return render_template('interest.html', interests=interests, user_interest=user_interest_list, user=user, image_file=image_file, form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, data_nasc=form.data_nasc.data, start_work_date=form.start_work_date.data, work_state=form.work_state.data,
                    work_city=form.work_city.data, salary=form.salary.data, instruction=form.instruction.data, company=form.company.data, card_number=0, card_name='', expiration_date='', cvv='', user_type='free')
        db.session.add(user)
        db.session.commit()
        flash('Sua conta acaba de ser criada. Você já pode acessar o sistema!', 'success')        
        return redirect(url_for('user_interests', username=user.username))
    return render_template('register.html', title='Registro', form=form)


@app.route("/register_premium", methods=['GET', 'POST'])
def register_premium():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    form = RegistrationFormPremium()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, data_nasc=form.data_nasc.data, start_work_date=form.start_work_date.data, work_state=form.work_state.data, work_city=form.work_city.data,
                    salary=form.salary.data, instruction=form.instruction.data, company=form.company.data, card_number=form.card_number.data, card_name=form.card_name.data, expiration_date=form.expiration_date.data, cvv=form.cvv.data, user_type='premium')
        db.session.add(user)
        db.session.commit()
        flash('Sua conta acaba de ser criada. Você já pode acessar o sistema!', 'success')
        return redirect(url_for('user_interests', username=user.username))
    return render_template('register_premium.html', title='Conta Premium', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.data_nasc = form.data_nasc.data
        current_user.start_work_date = form.start_work_date.data
        current_user.work_state = form.work_state.data
        current_user.work_city = form.work_city.data
        current_user.salary = form.salary.data
        current_user.instruction = form.instruction.data
        current_user.company = form.company.data
        current_user.card_number = form.card_number.data
        current_user.card_name = form.card_name.data
        current_user.expiration_date = form.expiration_date.data
        current_user.cvv = form.cvv.data
        db.session.commit()
        flash('your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.data_nasc.data = current_user.data_nasc
        form.start_work_date.data = current_user.start_work_date
        form.work_state.data = current_user.work_state
        form.work_city.data = current_user.work_city
        form.salary.data = current_user.salary
        form.instruction.data = current_user.instruction
        form.company.data = current_user.company
        form.card_number.data = current_user.card_number
        form.card_name.data = current_user.card_name 
        form.expiration_date.data = current_user.expiration_date 
        form.cvv.data = current_user.cvv
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend="Update Post")


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    form = request.form
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=form['username']).first()
    if user is None:
        posts = Post.query.filter_by(author=current_user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=5)
        flash('Usuario não existe', category="message")
        return render_template('feed.html', posts=posts)

    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
