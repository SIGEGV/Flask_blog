import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_blog.forms import RegistrationForm, LoginForm, updateAccountForms, PostForm
from flask_blog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog.models import User, Post


# both route retuen the same things;
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    # the post will be paginated in descending order i.e latest first and oldest at the end
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=post)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


#  a new route for Sign Up
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        # pushing data in data base and hashing the password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account Created Succesfully ", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Sign-Up", form=form)


#  a new route for logging in
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # if we are log out it will take us to the login page and then if we log in then we will be redirexted to
            # account page insted of home page
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Log in unsuccesfull, check Email and Password", "danger")
    return render_template("login.html", title="Login", form=form)


#  a new route for logging out
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


#  a function to update the profile picture;
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # this os.path.splitext(form_picture.filename) gives 2 value file name without extention
    #  and extention of the file name.
    _, f_ext = os.path.splitext(form_picture.filename)
    # we created a new name for the updated file
    picture_fn = random_hex + f_ext
    #  os.path.join   will simply copy the image from user device and will save it into our pics folder;
    picture_path = os.path.join(app.root_path, "static/pics", picture_fn)
    # resizing the picture to 125 pixel to save size of the filesystem
    #    wwe used Pillow lib from the Python to resize the image;
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


# a new route for account management
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = updateAccountForms()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account Updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    imagefile = url_for("static", filename="pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=imagefile, form=form)


# route for posting stuff
@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, Author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!!!!!!", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")


#  a route to redirect a user to Post
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


#  this is a route to update the POST
@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.Author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post Updated", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update_Post", form=form, legend="Update Post")


#  this is a route to Delete the POST
@app.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.Author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post Deleted", "success")
    return redirect(url_for("home"))


#  a new route for seeing only the post posted by a perticular user;
@app.route("/user/<string:username>")
def user_post(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # the post will be paginated in descending order i.e latest first and oldest at the end
    post = Post.query.filter_by(Author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template("user_post.html", posts=post, user=user)
