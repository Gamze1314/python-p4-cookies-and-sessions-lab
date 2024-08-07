#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    #GET /articles
    articles = Article.query.all()

    response_body = [article.to_dict() for article in articles]

    return jsonify(response_body), 200

@app.route('/articles/<int:id>')
def show_article(id):
    #each user can see maximum of 3 articles before seeing the paywall.
    #when a user makes a get request to /articles/<int:id>,
    # increment the session['page_views'] by 1.
    session['page_views'] = session.get('page_views', 0) + 1

    article = Article.query.get_or_404(id)

    if session['page_views'] <= 3:
        return jsonify(article.to_dict()), 200
    else:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    #if this is the first request, set session['page_views'] to an initial value of 0.(ternary)
    #for every request, increment value by 1.
    # If the user has viewed 3 or fewer pages, render a JSON response with the article data
    # If the user has viewed more than 3 pages, render a JSON response including an error message {'message': 'Maximum pageview limit reached'}, and a status code of 401 unauthorized

    # An API endpoint at /clear is available to clear your session as needed.
    


if __name__ == '__main__':
    app.run(port=5555)
