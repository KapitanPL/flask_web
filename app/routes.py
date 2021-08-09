from flask import render_template, redirect, url_for, request
from flask_login.utils import login_required
from app import app, db
from app.models import Article, Tag, Comment, User
from app.forms import CommentForm, LoginForm, NewPostForm
from flask_login import login_user, logout_user
from werkzeug.utils import secure_filename
import os

@app.route('/')
@app.route('/index')
def index():
        posts = Article.query.order_by(
                    Article.timestamp.desc())
        tags = Tag.query.order_by(Tag.used.desc())
        return render_template('index.html',posts=posts,tags=tags)

@app.route('/kapitannamustku', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
       user = User.query.get(1)
       if user is None or not user.check_password(form.password.data):
           return redirect(url_for('login'))
       login_user(user)
       return index()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(request.referrer)

@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
       if not os.path.exists('uploads'):
              os.mkdir('uploads')
       filename = secure_filename(form.file.data.filename)
       form.file.data.save('uploads/' + filename)
       tag_strings = form.tags.data.split(';')
       tags = list()
       for tag in tag_strings:
              tags.append(Tag.addTagRecord(tag))
       Article.addnewArticle('uploads/' + filename, form.name.data, form.abstract.data, tags, None)
       return index()
    posts = Article.query.order_by(
                    Article.timestamp.desc())
    tags = Tag.query.order_by(Tag.used.desc())
    return render_template('new_post.html',posts=posts,tags=tags, form=form)

@app.route('/<tag_id>/tagged', methods=['GET'])
def tagged(tag_id):
       posts = Article.getTaggedArticles(tag_id).order_by(Article.timestamp.desc())
       tags = Tag.query.order_by(Tag.used.desc())
       tag = Tag.query.filter( Tag.id == tag_id ).first_or_404()
       return render_template('index.html',posts=posts,title=tag.value, tags=tags, section_title="Články s tagem {0}".format(tag.value))

@app.route('/<post_id>/post', methods=['GET', 'POST'])
def post(post_id):
       commentForm = CommentForm()
       post = Article.query.filter( Article.id == post_id ).first_or_404()
       if ( commentForm.validate_on_submit() ):
              newComment=Comment(name=commentForm.name.data, text=commentForm.text.data, article=post)
              db.session.add(newComment)
              db.session.commit()
              return redirect(url_for('post', post_id=post_id))
       tags = Tag.query.order_by(Tag.used.desc())
       content = post.getContent()
       displayComments = Comment.query.filter( Comment.article_id == post_id).order_by(Comment.timestamp.desc())
       return render_template('post.html',title=post.name,tags=tags,post=post,content=content,form=commentForm,comments=displayComments)
