# -*- coding: utf-8 -*-
import datetime
from werkzeug.security import check_password_hash
from flask import url_for
from ex import db, app
from hashlib import md5

class Comment(db.EmbeddedDocument):
    # Global Commentary class
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name=u"Comment", required=True)
    author = db.StringField(verbose_name=u"Name", max_length=255, required=True)


class Stats(db.EmbeddedDocument):
    # User statistics class
    event_at = db.DateTimeField(default=datetime.datetime.now, required=False)
    event = db.StringField(verbose_name=u"Stats", required=False)
    referrer = db.StringField(verbose_name=u"Referrer", required=False)
    ip_addr = db.StringField(max_length=32, required=False)

class User(db.Document):
    # Users class for administration use
    _id = db.StringField(max_length=255, required=True)
    login = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=True)
    isadmin  = db.BooleanField(required=True)
    address  = db.StringField(max_length=255, required=False)
    firstname = db.StringField(max_length=255, required=False)
    secondname = db.StringField(max_length=255,required=False)
    email = db.StringField(max_length=255,required=False)
    last_seen = db.DateTimeField(default=datetime.datetime.now, required=True)
    about = db.StringField(verbose_name=u"About", required=True)
    stats = db.ListField(db.EmbeddedDocumentField('Stats'))



    def add_stats(self, event, event_at, referrer, ip_addr):
        '''
           This is method to add some information about user actions and events
           in DB by new embeded document

           :param event: The define about event Login, Logout and other
           :type event: Str
           :param event_at: event_at: Date and time when it was
           :type event_at: DateTime

           :param referrer: Url user comin from
           :type referrer: string
        '''
        user = self.get()
        stats = Stats()
        stats.event = event
        stats.event_at = event_at
        stats.referrer = referrer
        stats.ip_addr = ip_addr
        user.stats.append(stats)
        return user.save()

    def get_stats(self):
        return self.stats.get()

    def clear_stats(self):
        i = 0
        while i< len(self.stats):
            if self.stats:
                self.stats.pop()
        self.save()
        return

    def avatar(self, size):
        if self._id:
            return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def get(self):#userid
        user = User.objects.get_or_404(_id=self._id)
        if not user:
            return None
        return user


    def get_absolute_url(self):
        return url_for('user', kwargs={"user": self._id})

    def __repr__(self):
        return '<User %r>' % (self._id)


    def __unicode__(self):
        return self._id

    # Standard Defs
    def is_authenticated(self):
     return True


    def is_active(self):
        return True


    def is_anonymous(self):
     return False


    def get_id(self):
     return self._id




    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)  # embeded func for calculate hash

    meta = {
       'allow_inheritance': True,
      'indexes': ['_id'],
      'ordering': ['_id']
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
