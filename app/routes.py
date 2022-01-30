from flask import render_template, redirect, url_for, request
from flask_login.utils import login_required
from app import app, db
from app.models import Article, Tag, Comment, User
from app.forms import CommentForm, LoginForm, NewPostForm, EditTag
from flask_login import login_user, logout_user
import json
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
       tag_strings = form.tags.data.split(';')
       tags = list()
       for tag in tag_strings:
              tags.append(Tag.addTagRecord(tag))
       Article.addnewArticle(form.text.data , form.name.data, form.abstract.data, tags, None)
       return index()
    posts = Article.query.order_by(
                    Article.timestamp.desc())
    tags = Tag.query.order_by(Tag.used.desc())
    return render_template('new_post.html',posts=posts,tags=tags, form=form)

@app.route('/<post_id>/edit_post', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
       this_post = Article.query.filter( Article.id == post_id).first_or_404()
       form = NewPostForm()
       if form.validate_on_submit():
              tag_strings = form.tags.data.split(';')
              tags = list()
              for tag in tag_strings:
                     tags.append(Tag.addTagRecord(tag))
              this_post.name = form.name.data
              this_post.abstract = form.abstract.data
              this_post.updateContent( form.text.data )
              db.session.commit()
              return redirect(url_for('post', post_id=post_id))
       form.name.data = this_post.name
       tagString = str()
       for tag in this_post.tags:
              if tagString:
                     tagString += ";"
              tagString += tag.value
       form.tags.data = tagString
       form.abstract.data = this_post.abstract
       form.text.data = this_post.getContent(raw = True)
       posts = Article.query.order_by(
                    Article.timestamp.desc())
       tags = Tag.query.order_by(Tag.used.desc())
       return render_template('new_post.html',posts=posts,tags=tags, form=form)

@app.route('/<tag_id>/tagged', methods=['GET'])
def tagged(tag_id):
       posts = Article.getTaggedArticles(tag_id).order_by(Article.timestamp.desc())
       tags = Tag.query.order_by(Tag.used.desc())
       tag = Tag.query.filter( Tag.id == tag_id ).first_or_404()
       description = tag.description.replace("\n","<br>")
       return render_template('index.html',posts=posts,title=tag.value, tags=tags, section_title="#{0}".format(tag.value), section_body=description)

@app.route('/<post_id>/post', methods=['GET', 'POST'])
def post(post_id):
       commentForm = CommentForm()
       post = Article.query.filter( Article.id == post_id ).first_or_404()
       if ( commentForm.validate_on_submit()):
              newComment=Comment(name=commentForm.name.data, text=commentForm.text.data, article=post)
              db.session.add(newComment)
              db.session.commit()
              return redirect(url_for('post', post_id=post_id))
       tags = Tag.query.order_by(Tag.used.desc())
       content = post.getContent()
       displayComments = Comment.query.filter( Comment.article_id == post_id).order_by(Comment.timestamp.desc())
       return render_template('post.html',title=post.name,tags=tags,post=post,content=content,form=commentForm,comments=displayComments)

@app.route('/tags', methods=['GET', 'POST'])
@login_required
def tags():
       tags = Tag.query.order_by(Tag.description.desc())
       tagForm = EditTag(form_name='EditTags')
       tagForm.tagSelect.choices = [ tag.value for tag in tags ]
       if( tagForm.validate_on_submit() ):
              targetTag = Tag.query.filter( Tag.value == tagForm.tagSelect.data ).first()
              targetTag.description = tagForm.text.data
              db.session.commit()
              return redirect(url_for('tags'))
       tagForm.text.data = tags[0].description
       tagContent={ tag.value : tag.description for tag in tags }
       tagContent=json.dumps(tagContent)
       return render_template('tags.html', title="tagy", tags=tags, form=tagForm, tagsContent=tagContent)

@app.route('/<comment_id>/delete_comment', methods=['GET', 'POST'])
@login_required
def delete_comment( comment_id ):
       comment = Comment.query.filter( Comment.id == comment_id ).first_or_404()
       post_id = comment.article_id
       db.session.delete(comment)
       db.session.commit()
       return redirect(url_for('post', post_id=post_id))

@app.route('/caterpillar')
def caterpillar():
       return redirect(url_for('static',filename='caterpillarDream/index.html'))
