from flask import  render_template,url_for,flash,redirect,request
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog import app,db,bcrypt
from flask_login import login_user, current_user,logout_user,login_required
from flask_blog.models import User,Post

posts=[
    {
        'author': 'Yash Dobriyal',
        'title': 'First Blog',
        'content': 'first Post contents',
        'date': 'April 20, 2018'
    },
    
     {
        'author': 'John Doe',
        'title': 'second Blog',
        'content': 'second Post contents',
        'date': 'April 22, 2018'
    }
]
# both route retuen the same things;
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')




@app.route('/register',methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # pushing data in data base and hashing the password
        user=User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account Created Succesfully ','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign-Up',form=form)





@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()   
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            # if we are log out it will take us to the login page and then if we log in then we will be redirexted to 
            # account page insted of home page 
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Log in unsuccesfull, check Email and Password','danger')
    return render_template('login.html', title='Login',form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required 
def account():
    imagefile=url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account',image_file=imagefile)