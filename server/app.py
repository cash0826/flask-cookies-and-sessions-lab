#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Article, User, ArticleSchema, UserSchema

app = Flask(__name__)
CORS(app)
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
    articles = [ArticleSchema().dump(a) for a in Article.query.all()]
    return make_response(articles)

@app.route('/articles/<int:id>', methods = ['GET'])
def show_article(id):
    
    # Initialize the session for page views
    session['page_views'] = session.get('page_views') or 0
    
    # Increment the session on each request
    session['page_views'] += 1
    
    # If user has viewed 3 or fewer pages, render a JSON response with article data
    article = Article.query.filter(Article.id == id).first()
    if not article:
        return jsonify({'error': 'Article not found'})
    if session['page_views'] > 3:
        response = make_response(jsonify({
            "message": "Maximum pageview limit reached"
        }), 401)
        return response
    else:
        response = ArticleSchema().dump(article)
        return jsonify(response), 200    
   
if __name__ == '__main__':
    app.run(port=5555)
