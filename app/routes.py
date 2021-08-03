from flask import render_template, redirect, url_for
from app import app, db
from app.models import Article, Tag, Comment
from app.forms import CommentForm

@app.route('/')
@app.route('/index')
def index():
        posts = Article.query.order_by(
                    Article.timestamp.desc())
        tags = Tag.query.order_by(Tag.used.desc())
        return render_template('index.html',posts=posts,tags=tags)

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
