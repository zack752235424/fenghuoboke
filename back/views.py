
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash,check_password_hash

from back.models import User, Article, ArticleType, db
from utils.functions import is_login

back_blue = Blueprint('back',__name__)



@back_blue.route('/index/')
@is_login
def index():
    return render_template('/back/index.html')

@back_blue.route('/register/',methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('/back/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if username and password and password2:
            user = User.query.filter(User.username == username).first()
            if user:
                error = '警告！该账号已经注册，请更换账号'
                return render_template('/back/register.html',error = error)
            if password != password2:
                error = '警告！两次输入密码不一致'
                return render_template('/back/register.html',error=error)
            user = User()
            user.username = username
            user.password = generate_password_hash(password)
            user.save()
            return redirect(url_for('back.login'))
        else:
            error = '警告！请填写完整的信息'
            return render_template('/back/register.html',error = error)

@back_blue.route('/login/',methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('/back/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '警告！账号不存在，请去注册'
                return render_template('/back/login.html',error=error)
            if not check_password_hash(user.password,password):
                error = '警告！密码错误，请重新输入'
                return render_template('/back/login.html',error=error)
            session['user_id'] = user.id
            return redirect(url_for('back.index'))
        else:
            error = '警告！请填写完整的信息'
            return render_template('/back/login.html',error=error)

@back_blue.route('/logout/',methods = ['GET'])
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))

@back_blue.route('/a_type/',methods = ['GET'])
def a_type():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/category_list.html',types = types)

@back_blue.route('/add_type/',methods = ['GET','POST'])
def add_type():
    if request.method == 'GET':
        return render_template('/back/category_add.html')
    if request.method == 'POST':
        atype = request.form.get('atype')
        if not atype:
            error = '警告！请填写分类信息'
            return render_template('/back/category_add.html',error=error)
        art_type = ArticleType()
        art_type.t_name = atype
        db.session.add(art_type)
        db.session.commit()
        return redirect(url_for('back.a_type'))

@back_blue.route('/del_type/<int:id>/',methods = ['GET'])
def del_type(id):
    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.a_type'))

@back_blue.route('/article_list/',methods = ['GET'])
def article_list():
    usertype = session['user_id']
    articles = Article.query.filter(Article.usertype == usertype).all()
    return render_template('/back/article_list.html',articles = articles)

@back_blue.route('/article_detail/',methods = ['GET','POST'])
def article_add():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('/back/article_detail.html',types = types)
    if request.method == 'POST':
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        user_id = session['user_id']
        if title and desc and category and content:
            art = Article()
            art.title = title
            art.desc = desc
            art.content = content
            art.type = category
            art.usertype = user_id
            print(art)
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('back.article_list'))
        else:
            error = '请填写完整的文章信息'
            return render_template('/back/article_detail.html',error=error)

@back_blue.route('/user_list/',methods= ['GET'])
def user_list():
    users = User.query.all()
    return render_template('/back/user_list.html',users = users)

@back_blue.route('/del_user/<int:id>/',methods = ['GET'])
def del_user(id):
    user = User.query.get(id)
    user.is_delete = 1
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('back.user_list'))


@back_blue.route('/del_list/<int:id>/',methods = ['GET'])
def del_list(id):
    a_list = Article.query.get(id)
    db.session.delete(a_list)
    db.session.commit()
    return redirect(url_for('back.article_list'))


@back_blue.route('/edit/<int:id>',methods = ['GET','POST'])
def edit(id):
    if request.method == 'GET':
        types = ArticleType.query.all()
        a_edit = Article.query.get(id)
        return render_template('/back/edit.html',a_edit = a_edit,types = types)
    if request.method == 'POST':
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        if title and desc and category and content:
            art = Article.query.get(id)
            art.title = title
            art.desc = desc
            art.content = content
            art.type = category
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('back.article_list'))
        else:
            error = '请填写完整的文章信息'
            return render_template('/back/edit.html', error=error)