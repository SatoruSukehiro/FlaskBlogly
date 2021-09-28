"""Blogly application."""

from flask import Flask,render_template,redirect,request
from models import db, connect_db,User,Post,Tag,PostTag

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
    tags = Tag.query.all()
    return render_template('postform.html',tags=tags)

@app.route('/users/<int:user_id>/post/new',methods=["POST"])
def commitPost(user_id):
    user = User.query.get(user_id)
   
    
    
    new_post = Post(title=request.form['title'],content=request.form['content'],user=user)
    db.session.add(new_post)
    db.session.commit()
    for tag in request.form.getlist('tags'):
        posttags=PostTag(tag_id=tag,post_id=new_post.id)
        db.session.add(posttags)
    
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def getPost(post_id):
    post=Post.query.get(post_id)
    return render_template('postdetails.html',post=post)

@app.route('/posts/<int:post_id>/edit')
def editPost(post_id):
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    posttags = PostTag.query.all()
    return render_template('editpost.html',post=post ,tags=tags, posttags=posttags)


@app.route('/posts/<int:post_id>/edit',methods=['POST'])
def submitPost(post_id):
    post = Post.query.get(post_id)
    
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = request.form.getlist('tags')
    for tag in tag_ids:
        post_tags = PostTag(post_id=post.id, tag_id=tag)
        db.session.add(post_tags)
    db.session.commit()
    return redirect('/users')

@app.route('/posts/<int:post_id>/delete')
def deletePost(post_id):
    db.session.delete(Post.query.get(post_id))
    db.session.commit()
    return redirect("/users")
    







@app.route('/tags')
def get_tags():
    tags =  Tag.query.all()    
    return render_template('/tagslist.html',tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('/tagdetails.html',tag=tag)

@app.route('/tags/new')
def create_tag():
    
    return render_template('tagform.html')

@app.route('/tags/new',methods=["POST"])
def post_new_tag():
    new_tag = Tag(name=request.form['name'])
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag=Tag.query.get(tag_id)
    return render_template('edittags.html',tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])

def post_tag(tag_id):
    tag=Tag.query.get(tag_id)
    tag.name = request.form['name']
    posttags = PostTag.query.all()
    print(f'>>>>>>>>>>>>>>>>>>>>>{tag.posts}<<<<<<<<<<<<<<<<')
    db.session.commit()    
    return redirect('/tags') 

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')   