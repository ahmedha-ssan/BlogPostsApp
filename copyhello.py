from flask import Flask, render_template, flash,request,redirect,url_for
from subprocess import call
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , BooleanField,PasswordField, ValidationError
from wtforms.validators import DataRequired , EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime ,date
from flask_migrate import Migrate
from wtforms.widgets import TextArea
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,LoginManager,login_required,logout_user,current_user, UserMixin

app = Flask(__name__)
#Old sql DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Ourusers.db'
#New mysql DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mypassword@localhost/Ourusers'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = "my secret key"
#init databse
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

class Loginform(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])
    submit = SubmitField("Submit")

#create login page
@app.route('/login',methods=['GET','POST'])
def login():
    form = Loginform()
    if form.validate_on_submit():
        user = users.query.filter_by(username= form.username.data).first()
        if user:
            #check the hash
            if check_password_hash(user.password_hash , form.password.data):
                login_user(user)              
                flash("login successfully...")
                return redirect(url_for('dashboard'))
            else:
                flash("Worng password...")
        else:
            flash("User dosen't exist...")

    return render_template('login.html',form=form)


#create logout page
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out...")
    return redirect(url_for('login'))

#create dashboard page
@app.route('/dashboard',methods=['GET','POST'])
@login_required  
def dashboard():

    return render_template('dashboard.html')

class userForm(FlaskForm):
    name = StringField("Name ",validators=[DataRequired()])
    username=StringField("User name ",validators=[DataRequired()])
    email = StringField("Email ",validators=[DataRequired()])
    fav_color=StringField("Favorite Color")
    password_hash = PasswordField('Password',validators=[DataRequired(),EqualTo('password_hash2',message='Password Must match confirm Password...')])
    password_hash2 = PasswordField('Confirm password',validators=[DataRequired()])
    submit = SubmitField("Submit")

#blog post model
class posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    datePosted = db.Column(db.DateTime, default = datetime.utcnow)
    slug = db.Column(db.String(255))

class postForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()],widget=TextArea())
    author =StringField("Author", validators=[DataRequired()])
    slug =StringField("Slug", validators=[DataRequired()])
    submit =SubmitField("Submit", validators=[DataRequired()])



@app.route('/posts')
def addposts():
    Posts = posts.query.order_by(posts.datePosted)
    return render_template("posts.html",Posts=Posts)



@app.route('/posts/<int:id>')
def eachPost(id):
    post = posts.query.get_or_404(id)
    return render_template('eachPost.html',post=post)


@app.route('/addPost',methods=['GET','POST'])
#@login_required
def add_post():
    form= postForm()
    if form.validate_on_submit():
        post=posts(title=form.title.data,content=form.content.data,author=form.author.data,slug=form.slug.data)
        form.title.data=''
        form.content.data=''
        form.author.data=''
        form.slug.data=''
        db.session.add(post)
        db.session.commit()
        flash("Blog post submitted successfully")
    return render_template("addPost.html",form=form)

@app.route('/post/delete/<int:id>')
def delPost(id):
    postToDeleted = posts.query.get_or_404(id)
    try:
        db.session.delete(postToDeleted)
        db.session.commit()
        flash("Blog post deleted successfully...")
        Posts = posts.query.order_by(posts.datePosted)
        return render_template("posts.html",Posts=Posts)
    except:
        flash("Error in deleting the blog post try again...")
        Posts = posts.query.order_by(posts.datePosted)
        return render_template("posts.html",Posts=Posts)
    
@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
@login_required
def editPost(id):
    post = posts.query.get_or_404(id)
    form = postForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated...")
        return redirect(url_for('eachPost',id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('editPost.html',form=form)

#json
@app.route('/date')
def getCorrectDate():
    fav_pizza = {"Ahmed": "cheese","Saad": "zbr" }
    return fav_pizza





#db model
class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username= db.Column(db.String(200), nullable = False,unique=True)
    name = db.Column(db.String(200), nullable = False)
    email =db.Column(db.String(200), nullable = False)
    fav_color= db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable atribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<Name %r>' % self.name


@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    userDelete = users.query.get_or_404(id)
    name = None
    form = userForm()
    try:
        db.session.delete(userDelete)
        db.session.commit()
        flash("User deleted successfully...")
        ourUsers = users.query.order_by(users.date_added)
        return render_template("add_user.html",form=form,name=name,ourUsers=ourUsers)
    except:
        flash("Ops there was a problem...")







#updata DB record
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    form = userForm()
    name_update = users.query.get_or_404(id)
    if request.method == "POST":
        name_update.name = request.form['name']
        name_update.username = request.form['username']
        name_update.email = request.form['email']
        name_update.fav_color = request.form['fav_color']
        try:
            db.session.commit()
            flash("User updated successfully")
            return render_template("update.html",form=form,name_update=name_update)
        except:
            flash("Error in update... ")
            return render_template("update.html",form=form,name_update=name_update)
    else:
        return render_template("update.html",form=form,name_update=name_update,id=id)


#create a name form flask
class NameForm(FlaskForm):
    name = StringField("Whats your name",validators=[DataRequired()])
    submit = SubmitField("Submit")

#create a password form flask
class PasswordForm(FlaskForm):
    email = StringField("Whats your Email",validators=[DataRequired()])
    password_hash = PasswordField("Whats your password",validators=[DataRequired()])
    submit = SubmitField("Submit")







@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = userForm()
    if form.validate_on_submit():
        user = users.query.filter_by(email = form.email.data).first() 
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, method='pbkdf2:sha256')
            user = users(username=form.username.data,name = form.name.data, email = form.email.data, fav_color = form.fav_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data 
        form.name.data = ''
        form.username.data=''
        form.email.data = ''
        form.fav_color.data =''
        form.password_hash.data = ''
        flash("user added Successfully...")
    ourUsers = users.query.order_by(users.date_added)
    return render_template("add_user.html",form=form,name=name,ourUsers=ourUsers)




@app.route('/')
def index():
    flash("Welcome to our Website")
    return render_template("index.html")



@app.route('/user/<name>')
def user(name):
    return render_template("user.html",name=name)




#custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

#custom internal server error pages
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500


#create password page
@app.route('/testPW',methods=['GET','POST'])
def testPW():
    email = None
    password = None
    PWCheck =None
    passed=None
    form = PasswordForm() 
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''
        PWCheck = users.query.filter_by(email=email).first()
        passed = check_password_hash(PWCheck.password_hash, password)
    return render_template("testPW.html",email=email,password=password,form=form,PWCheck=PWCheck,passed=passed)


#create name page
@app.route('/name',methods=['GET','POST'])
def name():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submitted Successfully...")
    return render_template("name.html",name=name,form=form)

with app.app_context():
    db.create_all()



if __name__ == '__main__':
    app.run()
