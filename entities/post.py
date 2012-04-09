from google.appengine.ext import ndb
import rank, logging

class Post(ndb.Model):
    title = ndb.StringProperty()
    upvotes = ndb.IntegerProperty()
    downvotes = ndb.IntegerProperty()
    description = ndb.StringProperty()
    date_posted = ndb.DateTimeProperty(auto_now_add=True)
    score = ndb.ComputedProperty(lambda self: rank.rank(self.upvotes, self.downvotes))
    
    @classmethod
    def get_by_score(cls):
        return cls.query().order(-cls.score)
        
    @classmethod
    def upvote(cls, key):
        post = ndb.Key(urlsafe=key)
        post = post.get()
        post.upvotes += 1
        post.put()
        return post

    @classmethod
    def downvote(cls, key):
        post = ndb.Key(urlsafe=key)
        post = post.get()
        post.downvotes += 1
        post.put()
        return post
        
    @classmethod
    def delete(cls, key):
        post = ndb.Key(urlsafe=key)
        post.delete()
        return