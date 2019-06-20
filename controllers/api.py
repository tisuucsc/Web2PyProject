# Here go your api methods.

MY_STRINGS = [
    'banana', 'ananas', 'pineapple', 'anchovie', 'derrian', 'apple', 'apostrophe',
]

def get_product_list():
    results = []
    rows = db().select(db.product.ALL)
    for row in rows:
        #star_record = db(db.stars.product_id == row.id).select(db.stars.rating)
        #total = star_record.sum()
        #num = db(db.stars.product_id == row.id).count()
        #value = total/num
        results.append(dict(
            id=row.id,
            product_name=row.product_name,
            product_description=row.product_description,
            sales_price=row.sales_price,
            average = row.average
            # average_rating = (db().select(db.stars.product_id = row.id).count())
        ))
 
    return response.json(dict(post_list=results))

def search():
    s = request.vars.search_string or ''
    res = []
    rows = db().select(db.product.ALL)
    for row in rows:
        if row.product_name.startswith(s):
            res.append(dict(
                id = row.id,
                product_name=row.product_name,
                product_description= row.product_description,
                sales_price = row.sales_price,
                average = row.average,
                desired_quantity = 0,
                _details = False
            ))
    return response.json(dict(product_list=res))

@auth.requires_signature(hash_vars=False)
def set_stars():
    """Sets the star rating of a post."""
    post_id = int(request.vars.product_id)
    rating = int(request.vars.rating)
    db.user_star.update_or_insert(
        (db.user_star.post_id == post_id) & (db.user_star.user_email == auth.user.email),
        post_id = post_id,
        user_email = auth.user.email,
        rating = rating
    )
    return "ok"

def get_reviews():
    product_id = int(request.vars.product)
    rows = db((db.stars.product_id == db.review.product_id) & 
        (db.stars.user_email == db.review.user_email)).select()
    res = []
    if auth.user is not None:
        curUser = auth.user.email
    else:
        curUser = None
    for row in rows:
        if row.stars.product_id == product_id:
            user = db.auth_user(db.auth_user.email == row.stars.user_email)
            if row.stars.user_email != curUser:
                res.append(dict(
                    id = product_id,
                    name = user.first_name +" "+ user.last_name,
                    stars = row.stars.rating,
                    review = row.review.review_content
                ))
    return response.json(dict(review_list=res))

def get_own_review():
    product_id = int(request.vars.product)
    res = []
    if auth.user is None:
        res.append(dict(
                    id = product_id,
                    name = "",
                    stars = 0,
                    review = "",
                    _num_stars_display = 0
                ))
        return response.json(dict(review=res))
    curUser = auth.user.email
    rows = db((db.stars.product_id == db.review.product_id) & 
        (db.stars.user_email == db.review.user_email)).select()
    for row in rows:
        if row.stars.product_id == product_id:
            user = db.auth_user(db.auth_user.email == row.stars.user_email)
            if user.email == curUser:
                res.append(dict(
                    id = product_id,
                    name = user.first_name +" "+ user.last_name,
                    stars = row.stars.rating,
                    review = row.review.review_content,
                    _num_stars_display = row.stars.rating
                ))
    return response.json(dict(review=res))

def initializereview():
    product_id = int(request.vars.product)
    if auth.user is None:
        return None
    row = db.review(user_email = auth.user.email, product_id = product_id)
    if not row:
        db.review.insert(user_email = auth.user.email, product_id =product_id, review_content = "")
    row = db.stars(user_email = auth.user.email, product_id = product_id)
    if not row:
        db.stars.insert(user_email = auth.user.email, product_id =product_id, rating = 0)

def printthis(): 
    target = request.vars.target
    print target

def set_stars():
    product_id = request.vars.product_id
    rating = request.vars.rating
    if auth.user is None:
        return None
    row = db.stars(product_id = product_id, user_email = auth.user.email)
    row.update_record(rating = rating)
    getave(product_id)


def getave(id):
    rows = db(db.stars.product_id == id).select()
    count = 0
    curstarcount = 0
    for row in rows:
        if row.rating != 0:
            count += 1
            curstarcount += row.rating
    db(db.product.id == id).update(total = count, starcount = curstarcount, average = curstarcount / count)

def add_review():
    db(db.review.id == request.vars.product_id).update(review_content = request.vars.post_content)

@auth.requires_signature(hash_vars=False)
def inc_cart():
    db.shopping_cart.update_or_insert((db.shopping_cart.product_id == request.vars.product_id) & 
                                        (db.shopping_cart.user_email == auth.user.email),
                                        amount = request.vars.quantity, product_id = request.vars.product_id, user_email = auth.user.email)

def get_cart(): 
    res = []
    if auth.user == None:
        return response.json(dict(cart=res))
    curUser = auth.user.email
    rows = db(db.shopping_cart.user_email == curUser).select()
    for row in rows:
        products = db(db.product.id == row.product_id).select()
        for product in products:
            product_name = product.product_name
            price = product.sales_price
        res.append(dict(
            product = product_name,
            quantity = row.amount,
            cost = price * row.amount
        ))
    return response.json(dict(cart=res))

def clear_cart():
    db(db.shopping_cart.user_email == auth.user.email).delete()



