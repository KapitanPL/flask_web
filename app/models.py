from datetime import datetime
from enum import unique
from app import db
from markupsafe import Markup
import markdown

tagged = db.Table('tagged',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class ArticleCache:
    taggedArticles = None

    def __init__(self):
        self._tags = None
        self._formatedAbstract = None
        self._content = None

    def clearCache(self):
        self.taggedArticles = None
        self._tags = None
        self._formatedAbstract = None
        self._content = None

    def setTags(self, article_id, tags):
        if self._tags is None:
            self._tags = dict()
        self._tags[article_id] = tags

    def getTags(self, article_id):
        if self._tags and article_id in self._tags:
            return self._tags[article_id]
        else:
            return None

    def clearTags(self, article_id):
        if self._tags and article_id in self._tags:
            self._tags.pop(article_id)

    def setAbstract(self, article_id, abstract):
        if self._formatedAbstract is None:
            self._formatedAbstract = dict()
        self._formatedAbstract[article_id] = abstract

    def getAbstract(self, article_id):
        if self._formatedAbstract and article_id in self._formatedAbstract:
            return self._formatedAbstract[article_id]
        else:
            return None

    def setContent(self, article_id, content):
        if self._content is None:
            self._content = dict()
        self._content[article_id] = content

    def getContent(self, article_id):
        if self._content and article_id in self._content:
            return self._content[article_id]
        else:
            return None


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(256), index=True, unique=True)
    image = db.Column(db.String(256), index=False, unique=False, default='svg/kapitan_logo_small.svg')
    name = db.Column(db.String(256), index= True, unique=False)
    abstract = db.Column(db.String(2048), index=False, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tags = db.relationship("Tag",
        secondary=tagged,
        back_populates="articles")
    comments = db.relationship('Comment', backref='article', lazy='dynamic')
    cache = ArticleCache()

    def addTag(self, tag):
        self.tags.append(tag)
        self.cache.clearTags(self.id)

    def getTags(self):
        tags = self.cache.getTags(self.id)
        if tags is None:
            self.cache.setTags(self.id, Tag.query.join(
                tagged, (tagged.c.tag_id == Tag.id)).filter( tagged.c.article_id == self.id ).all())
            tags = self.cache.getTags(self.id)
        return tags 

    def getFormatedAbstract(self):
        abstract = self.cache.getAbstract(self.id)
        if abstract is None:
            self.cache.setAbstract(self.id, Markup(self.abstract.replace("\n", "<br>")))
            abstract = self.cache.getAbstract(self.id)
        return abstract

    def getContent(self):
        mdFile = open(self.file, 'r')
        return markdown.markdown(mdFile.read(),extensions=['markdown.extensions.tables'] )

    @staticmethod
    def getTaggedArticles(tag_id):
        return Article.query.join(
            tagged, ( tagged.c.article_id == Article.id )).filter( tagged.c.tag_id == tag_id )

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), index=True, unique=True)
    used = db.Column(db.Integer, default=0)
    articles = db.relationship("Article",
        secondary=tagged,
        back_populates="tags")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2048), index=False, unique=False)
    name = db.Column(db.String(256),  index=False, unique=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def getTime(self):
        return self.timestamp.strftime('%d.%m. %Y - %H:%M')
    