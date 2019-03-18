from flask import Blueprint, render_template, url_for, request, redirect

from back.models import Article,ArticleType

web_blue = Blueprint('web',__name__)



@web_blue.route('/home/',methods = ['GET'])
def home():
        articles = Article.query.all()
        return render_template('/web/home.html',articles = articles)


@web_blue.route('/article/',methods = ['GET','POST'])
def article():
    types = ArticleType.query.all()
    articles = Article.query.all()
    return render_template('/web/article.html',articles = articles, types = types)


@web_blue.route('/resource/',methods = ['GET'])
def resource():
    return render_template('/web/resource.html')


@web_blue.route('/timeline/',methods = ['GET'])
def timeline():
    return render_template('/web/timeline.html')


@web_blue.route('/about/',methods = ['GET'])
def about():
    return render_template('/web/about.html')


@web_blue.route('/detail/<int:id>/',methods = ['GET'])
def detail(id):
    types = ArticleType.query.all()
    article = Article.query.get(id)
    return render_template('/web/detail.html',article = article,types=types)

@web_blue.route('/article_type/<int:id_t>/',methods = ['GET'])
def article_type(id_t):
    types = ArticleType.query.all()
    type = ArticleType.query.get(id_t)
    articles = type.arts
    return render_template('/web/article.html',articles = articles, types = types)


@web_blue.route('/search/',methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        keywords = request.form.get('keywords')
        if keywords:
            types = ArticleType.query.filter(ArticleType.t_name.contains('%s' % keywords)).all()
            if not types:
                error = '没有相关类型，请重新输入！！！'
                return render_template('/web/article.html',error=error)
            return render_template('/web/article.html',types=types)
        else:
            error = '请输入完整信息！！！'
            return render_template('/web/article.html', error=error)
