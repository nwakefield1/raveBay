# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

def index():
    return dict(message=T('Welcome to raveBay!'))

# function to add a listing
@auth.requires_login()
def add():
    grid = SQLFORM(db.listing)
    if grid.process().accepted:
        session.flash = T('added')
        redirect(URL('default', 'posting'))
    export_classes = dict(csv=True, json=False, html=False,
    tsv=False, xml=False, csv_with_hidden_cols=False,
    tsv_with_hidden_cols=False)
    return dict(grid=grid)

# Function to view a listing
@auth.requires_login()
def view():
    p = db.listing(request.args(0)) or redirect(URL('default', 'posting'))
    grid = SQLFORM(db.listing, record = p, readonly = True)
    button = A('return to listings', _class='btn btn-default', _href=URL('default', 'posting'))
    export_classes = dict(csv=True, json=False, html=False,
	tsv=False, xml=False, csv_with_hidden_cols=False,
	tsv_with_hidden_cols=False)
    return dict(p=p, button = button)

# function to edit listings
@auth.requires_login()
def edit():
    p = db.listing(request.args(0)) or redirect(URL('default', 'posting'))
    if p.user_id != auth.user_id:
        session.flash = T('You are not authorized!')
        redirect(URL('default', 'posting'))
    grid = SQLFORM(db.listing, record=p)
    if grid.process().accepted:
        session.flash = T('updated')
        redirect(URL('default', 'view', args=[p.id]))
    export_classes = dict(csv=True, json=False, html=False,
    tsv=False, xml=False, csv_with_hidden_cols=False,
    tsv_with_hidden_cols=False)
    return dict(grid=grid)

# function to delete listings
@auth.requires_login()
@auth.requires_signature()
def delete():
    p = db.listing(request.args(0)) or redirect(URL('default', 'posting'))
    if p.user_id != auth.user_id:
        session.flash = T('You are not authorized!')
        redirect(URL('default', 'posting'))
    confirm = FORM.confirm('delete listing')
    grid = SQLFORM(db.listing, record = p, readonly = True, upload = URL('download'))
    if confirm.accepted:
        db(db.listing.id == p.id).delete()
        session.flash = T('listing is deleted')
        redirect(URL('default', 'posting'))
    export_classes = dict(csv=True, json=False, html=False,
    tsv=False, xml=False, csv_with_hidden_cols=False,
    tsv_with_hidden_cols=False)
    return dict(p=p, grid=grid, confirm=confirm)

# toggle for sold
@auth.requires_login()
@auth.requires_signature()
def soldCheck():
    # an item to show the user the avalibility of a product
    item = db.listing(request.args(0)) or redirect(URL('default', 'posting'))
    item.update_record(sold = not item.sold) 
    redirect(URL('default', 'posting')) # Assuming this is where you want to go


# necessary controller to display profile images
@auth.requires_login()
def download():
    return response.download(request, db)

# controller for profile.html
# checks if you are viewing your profile or someone else's and sends data accordingly
# p = table for user
# r = table for reviews
# size = size of reviews
# button - sends user to postreview
@auth.requires_login()
def profile():
    if request.args(0):
        p = db.auth_user(request.args(0))
        reviewtable = "user"+str(request.args(0))+"reviews"
    elif auth.user.id:
        p = db.auth_user(auth.user.id)
        reviewtable = "user"+str(auth.user.id)+"reviews"
    r = reviewsdb(reviewsdb[reviewtable]).select()
    size = reviewsdb(reviewsdb[reviewtable]).count()
    button = A('Leave A Review', _class='btn btn-default',
               _href=URL('default', 'postreview',
               vars=dict(reviewtable=reviewtable, userid = request.args(0) or auth.user.id))
              )
    return dict(p=p, r=r, size=size, button=button,)

# page to leave a review
@auth.requires_login()
def postreview():
    tablename = request.vars.reviewtable
    reviewsdb[tablename]['author_name'].default = auth.user.first_name
    grid = SQLFORM(reviewsdb[tablename])
    if grid.process().accepted:
        session.flash = T('added')
        redirect(URL('default','profile', args=[request.vars.userid]))
    export_classes = dict(csv=True, json=False, html=False,
    tsv=False, xml=False, csv_with_hidden_cols=False,
    tsv_with_hidden_cols=False)
    return dict(grid=grid)

# controller for votes/likes increments the counter when like button is pressed
def voteProfile():
    listing = db.auth_user[request.vars.id]
    new_votes = listing.votes + 1
    listing.update_record(votes=new_votes)
    return str(new_votes)

# controller for posting.html
# displays all current ticket listings
def posting():
    #the posting to show the grid
    show_all = request.args(0) == 'all'
    q = (db.listing) if show_all else (db.listing.sold == False)
    export_classes = dict(csv=True, json=False, html=False,
         tsv=False, xml=False, csv_with_hidden_cols=False,
         tsv_with_hidden_cols=False)

# delete button
    def deleteButton(row):
        b = ''
        if auth.user_id == row.user_id:
            b = A('Delete', _class='btn btn-info', _href=URL('default', 'delete', args=[row.id], user_signature=True))
        return b

# edit button
    def editButton(row):
        b = ''
        if auth.user_id == row.user_id:
            b = A('Edit', _class='btn btn-info', _href=URL('default', 'edit', args=[row.id]))
        return b

# sold button
    def soldButton(row):
        b = ''
        if auth.user_id == row.user_id:
            b = A('change sold status', _class='btn btn-info', _href=URL('default', 'soldCheck', args=[row.id], user_signature=True))
        return b

# view button
    def viewButton(row):
        b = A('View', _class='btn btn-info', _href=URL('default','view',args=[row.id]))
        return b

# profile button
    def profileButton(row):
        b = A('Profile', _class='btn btn-info', _href=URL('default','profile',args=[row.user_id]))
        return b

# shortens the length of the descriptions on posting.html
    def shorterL(row):
        return row.messeged[:40]

    # all the buttons for posting.html
    links = [
        dict(header='', body = deleteButton),
        dict(header='', body = editButton),
        dict(header='', body = soldButton),
        dict(header='', body = viewButton),
        dict(header='', body = profileButton),
        ]

    if len(request.args) == 0:
        links.append(dict(header='Description', body = shorterL))
        db.listing.messeged.readable = False

    start_idx = 1 if show_all else 0
    export_classes = dict(csv=True, json=False, html=False,
    tsv=False, xml=False, csv_with_hidden_cols=False,
    tsv_with_hidden_cols=False)

# declear the grid once
    grid = SQLFORM.grid(q,
        args=request.args[:start_idx],
        fields=[db.listing.sold,
                db.listing.title,
                db.listing.price,
                db.listing.name,
                db.listing.user_id,
                db.listing.messeged,
                db.listing.date_posted,
                ],
        create=False,
        links=links,
        editable=False,
        deletable=False,
        csv=False,
        details=False,
        )

# to show all or only avalible items
    if show_all:
        button = A('See only avalible listing', _class='btn btn-default', _href=URL('default', 'posting'))
    else:
        button = A('See all listing', _class='btn btn-default', _href=URL('default', 'posting', args=['all']))

    return dict(grid=grid, button=button)


# definitions for any controllers related to registration / login
# creates a table for reviews when a user registers
# of the form: userXreviews
# X = userid
def create_review_table_on_register(form):
    tablename = "user"+str(auth.user.id)+"reviews"
    db.define_table(tablename,
                    Field('reviews', 'text'),
                    Field('author_name'),
                    )

# calls create_review_table_on_register on successful registration
def user():
    auth.settings.register_onaccept = create_review_table_on_register
    return dict(grid=auth())


# function for messaging
# notfiy user if a message is sent successfully or not
@auth.requires_login()
def messages():
    form = crud.create(db.private_messages)
    if form.accepts(request.vars, session):
        session.flash = 'Message Sent'
        redirect(URL(r=request,f='inbox'))
    elif form.errors:
        response.flash='Theres an error'
    return dict(form=form)

# a function to delete listings
@auth.requires_login()
@auth.requires_signature()
def deletemessage():
    p = db.private_messages(request.args(0)) or redirect(URL('default', 'inbox'))
    grid = SQLFORM(db.private_messages, record = p, readonly = True)
    db(db.private_messages.id == p.id).delete()
    session.flash = T('Message has been deleted')
    redirect(URL('default', 'inbox'))
    export_classes = dict(csv=True, json=False, html=False,
    tsv=False, xml=False, csv_with_hidden_cols=False,
    tsv_with_hidden_cols=False)
    return dict(p=p, grid=grid, confirm=confirm)

# function to view a message
@auth.requires_login()
def viewmessage():
    p = db.private_messages(request.args(0)) or redirect(URL('default', 'inbox'))
    grid = SQLFORM(db.private_messages, record = p, readonly = True)
    button = A('return to inbox', _class='btn btn-default', _href=URL('default', 'inbox'))
    export_classes = dict(csv=True, json=False, html=False,
    tsv=False, xml=False, csv_with_hidden_cols=False,
    tsv_with_hidden_cols=False)
    p.update_record(opened = not p.opened)
    return dict(p=p, button = button)

# the posting to show inbox messages
@auth.requires_login()
def inbox():
    show_all = request.args(0) == 'all'
    q = db(db.private_messages.toid == auth.user.id)
    export_classes = dict(csv=True, json=False, html=False,
         tsv=False, xml=False, csv_with_hidden_cols=False,
         tsv_with_hidden_cols=False)

# buttons for inbox system
    def deleteMsgButton(row):
        b = A('Delete', _class='btn btn-info', _href=URL('default', 'deletemessage', args=[row.id], user_signature=True))
        return b

    def viewMsgButton(row):
        b = A('View', _class='btn btn-info', _href=URL('default','viewmessage',args=[row.id]))
        return b


# shortens the length of the descriptions on posting.html
    def shorterDescription(row):
        return row.messages[:40]

    def shorterSubject(row):
        return row.subject[:20]

    # all the buttons for posting.html
    links = [
        dict(header='', body = viewMsgButton),
        dict(header='', body = deleteMsgButton),
        ]

    if len(request.args) == 0:
        db.private_messages.fromid.readable = True
        db.private_messages.subject.readable = True
        db.private_messages.messages.readable = True
        db.private_messages.timesent.readable = True
        #links.append(dict(header='Message', body = shorterDescription))

    start_idx = 1 if show_all else 0
    export_classes = dict(csv=True, json=False, html=False,
    tsv=False, xml=False, csv_with_hidden_cols=False,
    tsv_with_hidden_cols=False)

# declare the grid once
    grid = SQLFORM.grid(q,
        args=request.args[:start_idx],
        fields=[db.private_messages.fromid,
                db.private_messages.subject,
                db.private_messages.messages,
                db.private_messages.timesent,
                ],
        create=False,
        links=links,
        editable=False,
        deletable=False,
        csv=False,
        details=False,
        )

# to show all or only avalible items
    if show_all:
        button = A('See only unopened messages', _class='btn btn-default', _href=URL('default', 'inbox'))
    else:
        button = A('See all messages', _class='btn btn-default', _href=URL('default', 'inbox', args=['all']))

    return dict(private_messages=messages, grid=grid, button=button)
