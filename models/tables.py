# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.


db.define_table('product',
    Field('product_name'),
    Field('product_description', 'text'),
    Field('sales_price', 'double'),
    Field('total', 'integer', default = 0),
    Field('starcount', 'integer', default = 0),
    Field('average', 'double', default = 0)
)
db.product.id.readable = False
db.product.sales_price.requires = IS_FLOAT_IN_RANGE(0, 10**10, dot=".")

db.define_table('stars',
	Field('product_id', 'reference product'),
	Field('user_email'),
	Field('rating', 'integer', default=None),
)

db.define_table('review',
	Field('product_id', 'reference product'),
	Field('user_email'),
	Field('review_content', 'text'),
)

db.define_table('shopping_cart',
	Field('user_email'),
	Field('product_id', 'reference product'),
	Field('amount', 'integer'),
)

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
