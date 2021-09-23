"""Blogly application."""

from flask import Flask,render_template,redirect,request
from models import db, connect_db,User,Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def home():
    return redirect('/users')


@app.route('/users')
def getUsers():
    return render_template('userlist.html',users=User.query.all())

@app.route('/users/new', methods=["GET"])
def createUser():
    return render_template('form.html')

@app.route('/users/new',methods = ["POST"])
def addUser():
    first = request.form['first']
    last = request.form['last']
    url = request.form['url']
    if len(url) == 0:
        url = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.zsaaVp0tIiSnOK-1rYpBnwAAAA%26pid%3DApi&f=1"
    newUser = User(fname=first,lname=last,image=url)
    db.session.add(newUser)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def getUser(user_id):
    
    return render_template('profile.html',user=User.query.get(user_id),posts=Post.query.all())

@app.route('/users/<int:user_id>/edit', methods=['GET'])
def editUser(user_id):
    
    
    return render_template('edit.html',user=User.query.get(user_id))

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def submitEdit(user_id):
    user = User.query.get(user_id)
    user.fname = request.form['first']
    user.lname = request.form['last']
    user.image = request.form['url']
    db.session.commit()
    return redirect('/users')



@app.route('/users/<int:user_id>/delete')
def deleteUser(user_id):
    db.session.delete(User.query.get(user_id))
    db.session.commit()
    return redirect('/users')










@app.route('/users/<int:user_id>/post/new',methods=["GET"])
def createPost(user_id):
    
    return render_template('postform.html')

@app.route('/users/<int:user_id>/post/new',methods=["POST"])
def commitPost(user_id):
    user = User.query.get(user_id)
    new_post = Post(title=request.form['title'],content=request.form['content'],user=user)
    db.session.add(new_post)
    db.session.commit()
    return redirect("/users")

@app.route('/posts/<int:post_id>')
def getPost(post_id):

    return render_template('postdetails.html',post=Post.query.get(post_id))

@app.route('/posts/<int:post_id>/edit')
def editPost(post_id):
    post = Post.query.get(post_id)
    return render_template('editpost.html',post=post)


@app.route('/posts/<int:post_id>/edit',methods=['POST'])
def submitPost(post_id):
    post = Post.query.get(post_id)
    
    post.title = request.form['title']
    
    print(post.content , post.title)
    db.session.commit()
    return redirect('/users')

@app.route('/posts/<int:post_id>/delete')
def deletePost(post_id):
    db.session.delete(Post.query.get(post_id))
    db.session.commit()
    return redirect("/users")