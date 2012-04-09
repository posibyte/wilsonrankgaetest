#!/usr/bin/env python
#
# Add
## Upvote
## Downvote
# Remove
# 
#
import webapp2
import logging, json
from datetime import datetime
import rank
from webapp2_extras import jinja2, sessions
from entities import post as post1
from jinja2_factory import jinja2_factory
import random
import config

class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(factory=jinja2_factory)
        
    def render_response(self, filename, **template_args):
        self.response.write(self.jinja2.render_template(filename, **template_args))
        
    def dispatch(self):
        # Get a session store for this request
        self.session_store = sessions.get_store(request = self.request)
        
        try:
            # Dispatch request
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions
            self.session_store.save_sessions(self.response)
    
    @webapp2.cached_property
    def session(self):
        # Return a session using the default cookie key
        return self.session_store.get_session()
    
class MainHandler(BaseHandler):
    def get(self):
        list = post1.Post().get_by_score()
        
        try:
            status = self.session.get_flashes('status')[0][0]
            flash = self.session.get_flashes('message')[0][0]
        except IndexError: 
            status, flash = None, None
        self.render_response('index.html', list=list, status=status, flash=flash)
        
class PostHandler(BaseHandler):
    def post(self):
        if(self.session.get('authorized') == 'True'):
            p1 = post1.Post()
            p1.populate(title=self.request.get('title'),
                        description = self.request.get('description'),
                        upvotes = int(round(random.random() * 100)),
                        downvotes = int(round(random.random() * 100)),
                        date_posted = datetime.now())
            p1.put()
            self.session.add_flash('alert alert-success', key='status')
            self.session.add_flash('<strong>Posted</strong> successfully', key='message')
        else:
            self.session.add_flash('alert alert-error', key='status')
            self.session.add_flash('<strong>Cannot post.</strong> Are you authorized?', key='message')
        
        self.redirect(self.uri_for('index'))
        
class VoteHandler(BaseHandler):
    def post(self):
        p = post1.Post()
        key = self.request.get('value')
        votes = 0
        
        if(self.request.get('action') == 'upvote'):
            p = p.upvote(key)
            votes = p.upvotes
        elif(self.request.get('action') == 'downvote'):
            p = p.downvote(key)
            votes = p.downvotes
        
        self.response.write(json.dumps({ 'count' : votes, 'score' : p.score }))
        
class LoginHandler(BaseHandler):
    def post(self):
        if(self.request.get('Login') == 'a correct password'):
            self.session['authorized'] = 'True'
            self.session.add_flash('alert alert-success', key='status')
            self.session.add_flash('Authorized to post messages', key='message')
        else:
            self.session.add_flash('alert alert-error', key='status')
            self.session.add_flash('Incorrect authentication', key='message')
            
        self.redirect('/')

class DeleteHandler(BaseHandler):
     def post(self):
        logging.debug(self.session.get('authorized'))
        if(self.session.get('authorized') == 'True'):
            key = self.request.get('key')
            post1.Post().delete(key)
            self.response.write(json.dumps({}))
        else:
            self.abort(403)
        
        # if(self.request.get('Login') == 'a correct password'):
            # self.session['authorized'] = 'True'
            # self.session.add_flash('alert alert-success', key='status')
            # self.session.add_flash('Authorized to post messages', key='message')
        # else:
            # self.session.add_flash('alert alert-error', key='status')
            # self.session.add_flash('Incorrect authentication', key='message')
               
        
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name='index'),
    ('/post', PostHandler),
    ('/vote', VoteHandler),
    ('/login', LoginHandler),
    ('/delete', DeleteHandler)
], debug=True, config=config.config)
