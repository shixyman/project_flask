from flask import Flask, render_template, redirect, url_for, flash, request,session 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, DecimalField, FileField
from wtforms.validators import DataRequired, Email, Length,InputRequired,URL
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_login import login_required, LoginManager, login_user, logout_user, login_required, current_user
from flask_login import UserMixin
from flask_paginate import Pagination


# Create a Flask instance
app = Flask(__name__)
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database based on the user_id
    return Users.query.get(int(user_id))

#add Database old version
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# new mysql database
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root@localhost/db_rev'
#secret key
app.config['SECRET_KEY'] = "secret_wabbit"
# Flask-Login


#initialize the Database
app.app_context().push()
db = SQLAlchemy(app)
 
#Create Model

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    fullName = db.Column(db.String(100),nullable=False)
    userName = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    #Create A STRING
    def __repr__(self):
        return '<userName %r>' % self.userName
        
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return '<Review %r>' % self.id
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    object = db.Column(db.String(100), nullable=False)
    reviews = db.relationship('Review', backref='product', lazy=True)

    def __repr__(self):
        return '<Product %r>' % self.name

# Create a form class
class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    search_results = []

    if form.validate_on_submit():
        search_query = form.search.data
        search_results = perform_search(search_query)

    return render_template("index.html", form=form, search_results=search_results)

def perform_search(search_query):
    # Perform the search based on the search query
    # Implement your search logic here and return the search results
    # You can replace this code with your actual search implementation
    search_results = []

    # Example search logic
    if search_query:
        # Perform the search based on Product Name, Product Type, and Product Object
        # Replace this code with your actual search logic
        search_results = Product.query.filter(
            (Product.name.ilike(f'%{search_query}%')) |
            (Product.type.ilike(f'%{search_query}%')) |
            (Product.object.ilike(f'%{search_query}%'))
        ).all()

        
            
    return search_results

@app.route('/user/<name>')
@login_required
def user(name):
    return render_template("user.html", userName=name)



# Create custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


# Create a form class
class SignUpForm(FlaskForm):
    fullName = StringField("Full Name", validators=[DataRequired(), Length(min=6, max=50)])
    userName = StringField("User Name or NickName", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Email Address", validators=[DataRequired(), Email(), Length(min=6, max=30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=30)])
    submit = SubmitField("Sign Up!")


# Create a route decorator
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        fullName = form.fullName.data
        userName = form.userName.data
        email = form.email.data
        password = form.password.data

        existing_user = Users.query.filter_by(email=email).first()
        if existing_user is None:
            new_user = Users(fullName=fullName, userName=userName, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)  # Start the session for the newly registered user

            flash("Sign Up Submitted Successfully!")
            return redirect(url_for('user', name=userName))
        else:
            flash("Email is already in use. Please enter a different email.")
            return redirect(url_for('signup'))
    return render_template("signup.html", form=form)



# Create a form class
class SignInForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email(), Length(min=6, max=30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=30)])
    submit = SubmitField("Sign in!")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Perform user authentication and set the user's login state
        # Example: Check if the email and password are valid
        
        # Assuming the authentication is successful
        user = Users.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            flash("Sign IN Submitted Successfully!")
            return redirect(url_for('user', name=email))  # Redirect with the email parameter
        else:
            flash("Invalid email or password. Please try again.")
            return redirect(url_for('signin'))
    return render_template("signin.html", form=form)


class ContactForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    cemail = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    cemail = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        full_name = form.full_name.data
        cemail = form.cemail.data
        message = form.message.data

        # Process the form data here (e.g., send an email)
        # You can add your own code to handle form data (e.g., send an email)
        # Here's a simple example of printing the form data
        print(f"Full Name: {full_name}")
        print(f"Email: {cemail}")
        print(f"Message: {message}")

        flash("Thank you for your message! We will get back to you soon!")
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)

@app.route('/faq')
def faq():
    return render_template('faq.html')



class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[InputRequired()])
    product_type = StringField('Product Type', validators=[InputRequired()])
    product_object = StringField('Product Object', validators=[InputRequired()])
    rating_choices = [
        ('poor', 'Poor'),
        ('bad', 'Bad'),
        ('average', 'Average'),
        ('good', 'Good'),
        ('excellent', 'Excellent')
    ]
    rating = SelectField('Rating', choices=rating_choices, validators=[InputRequired()])
    comment = StringField('Comment')
    image_url = StringField('Image URL' )
    submit = SubmitField('Submit')
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # class ProductForm(FlaskForm):
    #     product_name = StringField('Product Name', validators=[InputRequired()])
    #     product_type = StringField('Product Type', validators=[InputRequired()])
    #     product_object = StringField('Product Object', validators=[InputRequired()])
    #     rating_choices = [
    #         ('poor', 'Poor'),
    #         ('bad', 'Bad'),
    #         ('average', 'Average'),
    #         ('good', 'Good'),
    #         ('excellent', 'Excellent')
    #     ]
    #     rating = SelectField('Rating', choices=rating_choices, validators=[InputRequired()])
    #     comment = StringField('Comment')
    #     image_url = StringField('Image URL', validators=[URL()])
    #     submit = SubmitField('Submit')

    form = ProductForm()

    if form.validate_on_submit():
        product_name = form.product_name.data
        product_type = form.product_type.data
        product_object = form.product_object.data
        rating = form.rating.data
        comment = form.comment.data
        image_url = form.image_url.data

        # Create a new Product instance
        product = Product(name=product_name, type=product_type, object=product_object)
        db.session.add(product)
        db.session.commit()

        # Create a new Review instance associated with the current user and the product
        review = Review(rating=rating, comment=comment, user=current_user, product=product)
        db.session.add(review)
        db.session.commit()

        # If an image URL is provided, add it to the review
        if image_url:
            review.image_url = image_url
            db.session.commit()

        flash("Product review submitted successfully!")
        return redirect(url_for('dashboard'))

    # Get existing reviews for the current user
    reviews = current_user.reviews

    return render_template('dashboard.html', form=form, reviews=reviews)




class EditReviewForm(FlaskForm):
    rating_choices = [
        ('poor', 'Poor'),
        ('bad', 'Bad'),
        ('average', 'Average'),
        ('good', 'Good'),
        ('excellent', 'Excellent')
    ]
    rating = SelectField('Rating', choices=rating_choices, validators=[InputRequired()])
    comment = TextAreaField('Comment', validators=[InputRequired(), Length(max=500)])
    product_name = StringField('Product Name', validators=[InputRequired()])
    product_type = StringField('Product Type', validators=[InputRequired()])
    product_object = StringField('Product Object', validators=[InputRequired()])
    image_url = StringField('Image URL')
    submit = SubmitField('Update')

@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    form = EditReviewForm(obj=review)

    if form.validate_on_submit():
        form.populate_obj(review)
        db.session.commit()
        flash('Review updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_review.html', form=form, review=review)


@app.route('/delete-review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    # Retrieve the associated product
    product = review.product

    # Delete the review and the associated product
    db.session.delete(review)
    db.session.delete(product)

    db.session.commit()
    flash("Review and associated product deleted successfully!")
    return redirect(url_for('dashboard'))


@app.route('/products', methods=['GET'])
def all_products():
    page = request.args.get('page', 1, type=int)
    per_page = 4
    products = Product.query.paginate(page=page, per_page=per_page)

    pagination = Pagination(page=page, per_page=per_page, total=products.total, css_framework='bootstrap4')

    return render_template('products.html', products=products, pagination=pagination)

@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        # Perform the logout process
        logout_user()
        flash("Logged out successfully!")
        return redirect(url_for('index'))
    else:
        return abort(405)  # Return a 405 error for non-POST requests





if __name__ == "__main__":
    app.run(debug=True)
    