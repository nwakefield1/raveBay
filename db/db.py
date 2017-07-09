# define the table we will be using
db.define_table('listing',
                Field('title'),
                Field('price', 'decimal(6,2)'),
                Field('sold', 'boolean'),
                Field('image', 'upload'),
                Field('name'),
                Field('user_id', db.auth_user),
                Field('phone'),
                Field('email'),
                Field('messeged', 'text'),
                Field('date_posted', 'datetime'),
                Field('account_info', 'text'),
                )

db.listing.user_id.writable = False
db.listing.user_id.readable = False
db.listing.name.writable = False
db.listing.date_posted.writable = False
db.listing.email.writable = False

db.listing.category.required = True

db.listing.sold.default = False

db.listing.messeged.label = 'Message'
db.listing.name.default = first_name()
db.listing.date_posted.default = datetime.utcnow()
db.listing.user_id.default = auth.user_id
db.listing.email.default = get_email()
db.listing.category.requires = IS_IN_SET(CATEGORY, zero = None)
db.listing.category.default = 'Misc'

# to check for proper price numbermesseged 
db.listing.price.requires = IS_DECIMAL_IN_RANGE(0, 100000.00, dot=".")
#error_message='The price should be in the range 0..100000.00')
