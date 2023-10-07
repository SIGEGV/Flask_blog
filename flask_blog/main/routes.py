from  flask import render_template, request,Blueprint
from flask_blog.models import Post

from flask import Blueprint
main=Blueprint('main',__name__) 


# both route retuen the same things;
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    # the post will be paginated in descending order i.e latest first and oldest at the end
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=post)