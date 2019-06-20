# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    return dict()

def products():
    query = db.product
    links = []

    grid = SQLFORM.grid(
        query, 
        field_id = db.product.id, 
        fields = [db.product.id, db.product.product_name,
            db.product.product_description,
            db.product.sales_price, db.product.total, db.product.starcount, db.product.average],
        links = links,
        details=False,
        create=True, editable=False, deletable=False,
        csv=False,
        user_signature=True, # We don't need it as one cannot take actions directly from the form.
    )
    return dict(grid=grid)

def review():
    query = ((db.review.product_id == db.stars.product_id) & (db.review.user_email == db.stars.user_email))
    links = []

    grid = SQLFORM.grid(
        query,
        field_id = db.review.id,
        fields = [db.review.id, db.review.product_id, db.review.user_email, db.review.review_content, db.stars.rating],
        links = links,
        details = False,
        create=True, editable=False, deletable=False,
        csv=False,
        user_signature=True, # We don't need it as one cannot take actions directly from the form.
    )

    return dict(grid=grid)

def cart():
    query = db.shopping_cart
    links = []
    grid = SQLFORM.grid(
        query, 
        field_id = db.shopping_cart.id, 
        fields = [db.shopping_cart.id, db.shopping_cart.user_email, db.shopping_cart.product_id, db.shopping_cart.amount],
        links = links,
        details=False,
        create=True, editable=False, deletable=False,
        csv=False,
        user_signature=True, # We don't need it as one cannot take actions directly from the form.
    )
    return dict(grid=grid)


@auth.requires_login()
def addrating():
    product = db(db.product.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('review', 'text'),
        Field('stars', 'integer')
    )
    if form.process().accepted:
        # We insert the result, as in add1.
        db.stars.insert(
            product_id = product.id,
            user_email = auth.user.email,
            rating = form.vars.stars
        )
        db.review.insert(
            product_id = product.id,
            user_email = auth.user.email,
            review_content = form.vars.review
        )
        product.total += form.vars.stars
        product.starcount += 1
        product.average = product.total / product.starcount
        product.update_record()
        # And we load default/index via redirect.
        redirect(URL('default', 'index'))
    # We ask web2py to lay out the form for us.
    logger.info("My session is: %r" % session)
    return dict(form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


