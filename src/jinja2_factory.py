import webapp2
from webapp2_extras import jinja2

def jinja2_factory(self):
    j = jinja2.Jinja2(self)
    j.environment.filters.update({
        # Set Filters
        'datetimeformat' : datetimeformat
    })
    j.environment.globals.update({
        # Set global variables
        'uri_for': webapp2.uri_for,
    })
    return j;
    
def datetimeformat(value, format='%H:%M / %m-%d-%Y'):
    return value.strftime(format)