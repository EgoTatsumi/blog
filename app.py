from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Article %r>'

# app.app_context().push()
# db.create_all()


@app.route('/')
@app.route('/home') # теперь на двух  страницах будет один и тот же код
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create_article', methods=['POST', 'GET'])
def article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "An error occurred while adding the article"
    else:
        return render_template('create_article.html')


@app.route('/posts')
def posts():
    # articles = Article.query.first() # берет одну первую запись из бд
    # articles = Article.query.all() # берет все записи из бд
    articles =Article.query.order_by(Article.date.desc()).all() # order eto sortirovka desc - sortirovka s samoy novoy dati
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id>/delete')
def delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "An error occurred while deleting"


@app.route('/posts/<int:id>/edit', methods=['POST', 'GET'])
def post_edit(id):
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "An error occurred while adding the article"
    else:
        article = Article.query.get(id)
        return render_template('post_edit.html', article=article)


# @app.route('/user/<string:name>/<int:id>') # обрвботка значнеия из url адреса
# def user(name, id):
#     return f'user page: {name}, {id}'


if __name__ == '__main__':
    app.run(debug=True)
