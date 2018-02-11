from flask import Flask, render_template, request, redirect, jsonify, url_for, make_response  # noqa
from sqlalchemy import and_, or_, desc, create_engine, exc
from sqlalchemy.orm import sessionmaker
from catalog_database_setup import Base, Category, Item
from flask import session as login_session
import random
import string
import httplib2
import json
import requests

from oauth2client.client import FlowExchangeError
from oauth2client.client import OAuth2WebServerFlow

app = Flask(__name__)

#CLIENT_ID = json.loads(
#    open('client_secrets.json', 'r').read())['web']['client_id']
CLIENT_ID = '247629617558-40cubh6aeg09oiul1snma5ghbdlqg4gr.apps.googleusercontent.com';
url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format('catalog', 'password', 'localhost', '5432', 'catalog_db')
engine = create_engine(url, client_encoding='utf8')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    # create anti forgery state
    state = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/')
@app.route('/catalog')
def index():
    logged_in = True
    if 'username' not in login_session:
        logged_in = False
    result_set = session.query(Category).all()
    categories = []
    for category in result_set:
        categories.append(category)
    # return latest items (items recently added)
    result_set = session.query(Item).order_by(desc(Item.id)).limit(10).all()
    latest_items = []
    for item in result_set:
        item.category = get_category_of_item(item)
        latest_items.append(item)
    return render_template(
        'index.html',
        categories=categories,
        items=latest_items,
        logged_in=logged_in)


@app.route('/catalog/<category_name>/items')
def show_items_view(category_name):
    logged_in = True
    if 'username' not in login_session:
        logged_in = False
    result_set = session.query(Category).all()
    categories = []
    items = []
    for category in result_set:
        if category.name == category_name:
            selectedCategory = category
            items = get_items_by_category(category)
            selectedCategory.item_count = len(items)
        categories.append(category)

    return render_template(
        'index.html',
        categories=categories, selectedCategory=selectedCategory,
        items=items, logged_in=logged_in)


'''
Adds a new item to catalog by processing the submitted form
and serves add item page. Only logged in users are able to add items.
'''


@app.route('/catalog/items/add', methods=['GET', 'POST'])
def add_item():
    logged_in = True
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'GET':
        result_set = session.query(Category).all()
        categories = []
        for category in result_set:
            categories.append(category)
        return render_template('addItem.html',
                               categories=categories, logged_in=logged_in)
    else:
        title = request.values.get('title')
        description = request.values.get('description')
        category_name = request.values.get('category')
        # get category object of new item by category name
        category = session.query(Category).filter_by(
            name=category_name).one()
        item = Item(
            name=title, description=description, category=category)
        session.add(item)
        session.commit()
        return redirect(url_for('index'))


'''
Updates given item of catalog by processing the submitted form
and serves updateItem page. Only logged in users are able to update items.
'''


@app.route('/catalog/<int:item_id>/update', methods=['GET', 'POST'])
def update_item(item_id):
    logged_in = True
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'GET':
        try:
            item = session.query(Item).filter_by(id=item_id).one()
        except exc.SQLAlchemyError:
            return redirect(url_for('index'))

        item.category = get_category_of_item(item)
        result_set = session.query(Category).all()
        categories = []
        for category in result_set:
            categories.append(category)
        return render_template(
            'updateItem.html',
            categories=categories,
            item=item,
            logged_in=logged_in)
    else:
        title = request.values.get('title')
        description = request.values.get('description')
        category_name = request.values.get('category')

        # get category object of new item by category name
        category = session.query(Category).filter_by(name=category_name).one()
        # find item
        item = session.query(Item).filter_by(id=item_id).one()

        item.name = title
        item.description = description
        item.category = category
        session.add(item)
        session.commit()
        return redirect(url_for('index'))


'''
Deletes given item from the catalog and serves deleteItem page
. Only logged in users are able to update items.
'''


@app.route('/catalog/<int:item_id>/delete', methods=['GET', 'POST'])
def delete_item(item_id):
    logged_in = True
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'GET':
        try:
            item = session.query(Item).filter_by(id=item_id).one()
        except exc.SQLAlchemyError:
            return redirect(url_for('index'))
        return render_template('deleteItem.html',
                               item=item, logged_in=logged_in)
    else:
        result_set = session.query(Item).filter_by(id=item_id)
        item = result_set[0]
        session.delete(item)
        session.commit()
        return redirect(url_for('index'))


'''
Serves itemDetail page for the given item
'''


@app.route('/catalog/<category_name>/<int:item_id>')
def show_item_description(category_name, item_id):
    logged_in = True
    if 'username' not in login_session:
        logged_in = False
    try:
        item = session.query(Item).filter_by(id=item_id).one()
    except exc.SQLAlchemyError:
        return redirect(url_for('index'))
    return render_template('itemDetail.html',
                           item=item, logged_in=logged_in)

# JSON Endpoint


@app.route('/catalog.json')
def get_catalog_json():
    result_set = session.query(Category).all()
    catalog = []
    for category in result_set:
        items = get_items_by_category(category)
        catalog.append(category_items_to_json(category, items))
    return jsonify(catalog)


@app.route('/catalog/category/<int:id>')
def get_category(id):
    result_set = session.query(Category).filter_by(id=id)
    return jsonify(
        category_items_to_json(
            result_set[0],
            get_items_by_category(
                result_set[0])))


@app.route('/catalog/item/<int:id>')
def get_item(id):
    result_set = session.query(Item).filter_by(id=id)
    return jsonify(item_to_json(result_set[0]))


'''
gconnect and gdisconnect are used to connect/disconnect a google account to
the application.
'''


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = OAuth2WebServerFlow(client_id='247629617558-40cubh6aeg09oiul1snma5ghbdlqg4gr.apps.googleusercontent.com',
        client_secret='7mzjfQEk2kbZZf-ygkf3ZaOl', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h3>You are now logged in as'
    output += login_session['username']
    output += '! Redirecting to home page...</h3>'

    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('index'))
    else:
        response = make_response(
            json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
        return response


'''
Helper functions.
'''


def get_items_by_category(category):
    result_set = session.query(Item).filter_by(category=category)
    items = []
    for item in result_set:
        items.append(item_to_json(item))
    return items


def get_category_of_item(item):
    result_set = session.query(Category).filter_by(id=item.category_id)
    return result_set[0]


def category_items_to_json(category, items):
    return {
        'id': category.id,
        'name': category.name,
        'items': items
    }


def category_to_json(category):
    return {
        'id': category.id,
        'name': category.name
    }


def item_to_json(item):
    return {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'category_id': item.category_id

    }


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run()
