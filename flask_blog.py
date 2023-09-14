from flask import Flask,render_template,url_for,flash,redirect
from forms import RegistrationForm, LoginForm
app=Flask(__name__)

# go to python cli and type improt secrets and then secrets.token_hex(16) and it will give you a randon 16 digit key value
app.config['SECRET_KEY']='b05103f9ee374fa043ba58ced99cfcb4'
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
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created For {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Sign-Up',form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
    # down code was used as tmp database;
        if form.email.data== 'admin@gmail.com' and form.password.data=='123456':
         flash('You have logged in !!!!!!!!','success')
         return redirect(url_for('home'))
        else:
            flash('Log in unsuccesfull, check username and password','danger')
    return render_template('login.html', title='Login',form=form)





if __name__ == '__main__':
    app.run(debug=True,port=8080)