from flask import Flask, jsonify

from storage import allArticles, liked_articles, unliked_articles
from demographic_filtering import output
from content_based_filtering import get_recommendations

app = Flask(__name__)

@app.route("/")
def home_page():
    return jsonify({
        "Message": "Go to '/get-article', '/liked-article' or '/unliked-article'"
    })

@app.route("/get-article")
def getArticle():
    article_data = {
        "url": allArticles[0][11],
        "title": allArticles[0][12],
        "text": allArticles[0][13],
        "lang": allArticles[0][14],
        "total_events": allArticles[0][15]
    }
    return jsonify({
        "data": article_data,
        "status": "Success!"
    })

@app.route("/liked-article", methods = ["POST"])
def likedArticle():
    article = allArticles[0]
    liked_articles.append(article)
    allArticles.pop(0)
    return jsonify({
        "status": "Success!"
    }), 201

@app.route("/unliked-article", methods = ["POST"])
def unlikedArticle():
    article = allArticles[0]
    unliked_articles.append(article)
    allArticles.pop(0)
    return jsonify({
        "status": "Success!"
    }), 201

@app.route("/popular-articles")
def popularArticles():
    article_data = []
    for article in output:
        _d = {
            "url": article[0],
            "title": article[1],
            "text": article[2],
            "lang": article[3],
            "total_events": article[4]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "Success!"
    }), 200

@app.route("/recommended-articles")
def recommendedArticles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[4])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "url": recommended[0],
            "title": recommended[1],
            "text": recommended[2],
            "lang": recommended[3],
            "total_events": recommended[4]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "Success!"
    }), 200

if __name__ == "__main__":
    app.run()