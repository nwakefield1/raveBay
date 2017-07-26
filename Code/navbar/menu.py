# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(IMG(_src='https://i.imgur.com/A2LRvVK.png',_alt="My Logo",_style= "margin:20px 10px"), _href=URL('default','index'))
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''
# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

#response.menu = [
#    (T('Home'), False, URL('default', 'index'), [])
#]

DEVELOPMENT_MENU = True


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources
    # Buttons and redirection for our navigation bar
    # ------------------------------------------------------------------------------------------------------------------
    response.menu += [
        (T('Home'), False, '/init/default/'),
        (T('Postings'), False, '/init/default/posting'),
        (T('My Profile'), False, URL('/profile')),
        (T('Messages'), False, URL('default','messages'),[]),
        (T('Inbox'), False,URL('default','inbox'), []),
        (T('Community'), False, 'http://webchat.freenode.net/?channels=raveBay')
    ]


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()
