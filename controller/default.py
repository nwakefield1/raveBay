# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

def index():
    response.flash = T("Welcome to raveBay")
    return dict(message=T('Welcome to web2py!'))

@auth.requires_login()
def add():
 # Function to add a listing
    grid = SQLFORM(db.listing)
    if grid.process().accepted:
        session.flash = T('added')
        redirect(URL('default', 'posting'))
    export_classes = dict(csv=True, json=False, html=False,
    tsv=False, xml=False, csv_with_hidden_cols=False,
    tsv_with_hidden_cols=False)

    return dict(grid=grid)
    
def view():
	# Function to view a listing
		p = db.listing(request.args(0)) or redirect(URL('default', 'posting'))
		grid = SQLFORM(db.listing, record = p, readonly = True)
		button = A('return to listings', _class='btn btn-default', _href=URL('default', 'posting'))
		export_classes = dict(csv=True, json=False, html=False,
		tsv=False, xml=False, csv_with_hidden_cols=False,
		tsv_with_hidden_cols=False)
		return dict(p=p, button = button)

@auth.requires_login()
def edit():
  # Function to edit listings
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

@auth.requires_login()
@auth.requires_signature()
def delete():
  # a fucntion to delete listings
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
    return dict(grid=grid, confirm=confirm)

@auth.requires_login()
@auth.requires_signature()
def soldCheck():
 # an item to show the user the avalibility of a product
     item = db.listing(request.args(0)) or redirect(URL('default', 'posting'))
     item.update_record(sold = not item.sold) 
     redirect(URL('default', 'posting')) # Assuming this is where you want to go

@auth.requires_login()
def download():
    return response.download(request, db)

@auth.requires_login()
def profile():
    p = db.auth_user(request.args(0))
    fname = p.first_name
    lname = p.last_name
    email = p.email
    ptext = p.profiletext
    pmage = p.profileimage
    return dict(fname=fname, lname=lname, email=email, ptext=ptext, pmage=pmage)

# @auth.requires_login()
def posting():
  # the posting to show the grid
    show_all = request.args(0) == 'all'
    q = (db.listing) if show_all else (db.listing.sold == False)
    export_classes = dict(csv=True, json=False, html=False,
         tsv=False, xml=False, csv_with_hidden_cols=False,
         tsv_with_hidden_cols=False)

# Delete button
    def deleteButton(row):
        b = ''
        if auth.user_id == row.user_id:
            b = A('Delete', _class='btn btn-info', _href=URL('default', 'delete', args=[row.id], user_signature=True))
        return b

# Edit button
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

# to make the description appear but shorter
    def shorterL(row):
        return row.messeged[:40]

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
                db.listing.date_posted,
                db.listing.user_id,
                db.listing.messeged,
                ],
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

def user():
    return dict(grid=auth())
