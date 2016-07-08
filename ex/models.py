# -*- coding: utf-8 -*-
import datetime
from flask import url_for
from ex import db


class Comment(db.EmbeddedDocument):
# Global Commentary class
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name=u"Comment", required=True)
    author = db.StringField(verbose_name=u"Name", max_length=255, required=True)


class Users(db.Document):
# Users class for administration use
    username = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=True)
    isadmin  = db.StringField(max_length=255, required=True)

    def get(userid):
        #u = db.getCollection('users').find({})
        u =app.config['USERS_COLLECTION']#.find_one({"_id": self.username})
        if not u:
            return None
        return Users(u['_id'])

    def __repr__(self):
        return '<User %r>' % (self.username)


    def __unicode__(self):
     return self.username

    meta = {
       'allow_inheritance': True,
      'indexes': ['username'],
      'ordering': ['username']
    }

class Post(db.Document):
    # Global class for load an article
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    body = db.StringField(required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
     }
