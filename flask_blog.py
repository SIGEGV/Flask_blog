from flask import Flask,render_template,url_for
app=Flask(__name__)

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
def hello():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True,port=8080)