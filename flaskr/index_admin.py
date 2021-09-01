### 蓝图
# 定义蓝图并注册到应用工厂。
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.user import login_required
from flaskr.db import get_db

bp = Blueprint('index_admin', __name__, url_prefix='/index_admin')

# 使用 app.register_blueprint() 在工厂中 导入和注册蓝图。将新代码放在工厂函数的尾部，返回应用之前



# 与验证蓝图不同，博客蓝图没有 url_prefix 。因此 index 视图会用于 / ， create 会用于 /create ，以此类推。
# 博客是 Flaskr 的主要 功能，因此把博客索引作为主索引是合理的。
# 但是，下文的 index 视图的端点会被定义为 my_datasets.index 。
# 一些验证视图 会指定向普通的 index 端点。 
# 我们使用 app.add_url_rule() 关联端点名称 'index' 和 / URL ，这样 url_for('index') 或 url_for('my_datasets.index') 都会有效，会生成同样的 / URL 。
# 在其他应用中，可能会在工厂中给博客蓝图一个 url_prefix 并定义一个独立的 index 视图，类似前文中的 hello 视图。在这种情况下 index 和 blog.index 的端点和 URL 会有所不同

### 索引
# 索引会显示所有帖子，最新的会排在最前面。为了在结果中包含 user 表中的 作者信息，使用了一个 JOIN 。
@bp.route('/')
def index():
    db = get_db()
    frames = db.execute(
        'SELECT f.id, title, directory, argument_number, created, author_id, username'
        ' FROM frame f JOIN user u ON f.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('index_admin/index_admin.html', frames=frames)


### 创建
# create 视图与 register 视图原理相同。
# 要么显示表单，要么发送内容 已通过验证且内容已加入数据库，或者显示一个出错信息。
# 先前写的 login_required 装饰器用在了博客视图中，这样用户必须登录以后 才能访问这些视图，否则会被重定向到登录页面
# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO post (title, body, author_id)'
#                 ' VALUES (?, ?, ?)',
#                 (title, body, g.user['id'])
#             )
#             db.commit()
#             return redirect(url_for('index_admin.index'))

#     return render_template('index_admin/index_admin.html')


### 更新
# update 和 delete 视图都需要通过 id 来获取一个 post ，并且 检查作者与登录用户是否一致。
# 为避免重复代码，可以写一个函数来获取 post ， 并在每个视图中调用它。
# def get_post(id, check_author=True):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, f"Post id {id} doesn't exist.")

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post
# abort() 会引发一个特殊的异常，返回一个 HTTP 状态码。
# 它有一个可选参数， 用于显示出错信息，若不使用该参数则返回缺省出错信息。 
# 404 表示“未找到”， 403 代表“禁止访问”。（ 401 表示“未授权”，但是我们重定向到登录 页面来代替返回这个状态码）
# check_author 参数的作用是函数可以用于在不检查作者的情况下获取一个 post 。
# 这主要用于显示一个独立的帖子页面的情况，因为这时用户是谁没有关系， 用户不会修改帖子。


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('index_admin.index'))

#     return render_template('index_admin/index_admin.html', post=post)
# 和所有以前的视图不同， update 函数有一个 id 参数。该参数对应路由中 的 <int:id> 。
# 一个真正的 URL 类似 /1/update 。 
# Flask 会捕捉到 URL 中的 1 ，确保其为一个 int ，并将其作为 id 参数传递给视图。 
# 如果没有指定 int: 而是仅仅写了 <id> ，那么将会传递一个字符串。 
# 要生成一个指向更新页面的 URL ，需要传递 id 参数给 url_for() ： url_for('my_datasets.update', id=post['id']) 。
# 前文的 index.html 文件中 同样如此。

# create 和 update 视图看上去是相似的。 
# 主要的不同之处在于 update 视图使用了一个 post 对象和一个 UPDATE 查询代替了一个 INSERT 查询。
# 作为一个明智的重构者，可以使用 一个视图和一个模板来同时完成这两项工作。
# 但是作为一个初学者，把它们分别处理 要清晰一些。


### 删除
# 删除视图没有自己的模板。删除按钮已包含于 update.html 之中，该按钮指向 /<id>/delete URL 。
# 既然没有模板，该视图只处理 POST 方法并重定向到 index 视图。
# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('index_admin.index'))