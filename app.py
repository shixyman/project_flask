
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
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
# import all modules needed in this projects

# Create a Flask instance
app = Flask(__name__)
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database based on the user_id
    return Users.query.get(int(user_id))

#add Database old version (using sqllite for test)
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

class Users(UserMixin, db.Model):
    # Define the Users table in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    fullName = db.Column(db.String(100), nullable=False)  # User's full name
    userName = db.Column(db.String(100), nullable=False)  # User's username
    email = db.Column(db.String(100), nullable=False, unique=True)  # User's email (must be unique)
    password = db.Column(db.String(100), nullable=False)  # User's password
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  # Date and time when the user was added
    reviews = db.relationship('Review', backref='user', lazy=True)  # Relationship to Review table

    def __repr__(self):
        return f"Users(id={self.id}, username='{self.userName}', email='{self.email}')"

    def __init__(self, fullName, userName, email, password, date_added):
        # Initialize the Users object with provided attributes
        self.fullName = fullName
        self.userName = userName
        self.email = email
        self.password = password
        self.date_added = date_added


class Review(db.Model):
    # Define the Review table in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each review
    rating = db.Column(db.String(20), nullable=False)  # Rating for the review
    comment = db.Column(db.Text)  # Comment for the review
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to Users table
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # Foreign key to Product table

    def __repr__(self):
        return '<Review %r>' % self.id


class Product(db.Model):
    # Define the Product table in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each product
    name = db.Column(db.String(100), nullable=False)  # Name of the product
    type = db.Column(db.String(100), nullable=False)  # Type/Category of the product
    object = db.Column(db.String(100), nullable=False)  # Object representation of the product
    reviews = db.relationship('Review', backref='product', lazy=True)  # Relationship to Review table

    def __repr__(self):
        return '<Product %r>' % self.name
    
# Create a form class
class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()]) # Text input field for search query
    submit = SubmitField('Submit') # Submit button for the form


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm() # Create an instance of the SearchForm
    search_results = [] # Initialize an empty list to store search results

    if form.validate_on_submit():
         # If the form is submitted and passes validation
        search_query = form.search.data # Get the search query from the form
        search_results = perform_search(search_query)# Perform the search based on the query

    return render_template("index.html", form=form, search_results=search_results)# Render the index.html template with the form and search results

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

        
            
    return search_results # Return the search results

@app.route('/user/<name>')
@login_required
def user(name):
    return render_template("user.html", userName=name)
     # Render the user.html template and pass the username as a parameter


# Create custom error pages
# Error handler for 404 - Page Not Found error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
    # Render the "404.html" template and return a 404 status code

# Error handler for 500 - Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500
    # Render the "500.html" template and return a 500 status code


# Create a form class
class SignUpForm(FlaskForm):
    fullName = StringField("Full Name", validators=[DataRequired(), Length(min=6, max=50)])# Text input field for full name
    userName = StringField("User Name or NickName", validators=[DataRequired(), Length(min=3, max=50)])# Text input field for username
    email = StringField("Email Address", validators=[DataRequired(), Email(), Length(min=6, max=30)])# Text input field for email address
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=30)])# Password input field for password
    submit = SubmitField("Sign Up!")# Submit button for the form


# Create a route decorator
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm() # Create an instance of the SignUpForm
    if form.validate_on_submit():   # If the form is submitted and passes validation
        fullName = form.fullName.data # Get the full name from the form
        userName = form.userName.data # Get the username from the form
        email = form.email.data # Get the email address from the form
        password = form.password.data # Get the password from the form

        existing_user = Users.query.filter_by(email=email).first()  # Check if a user with the same email already exists in the database
        if existing_user is None:  # If the email is not already in use
            new_user = Users(fullName=fullName, userName=userName, email=email, password=password,date_added=datetime.utcnow() ) # Create a new user object with the provided information
            db.session.add(new_user) # Add the new user to the database session
            db.session.commit()  # Commit the changes to the database

            login_user(new_user)  # Start the session for the newly registered user

            flash("Sign Up Submitted Successfully!")
            return redirect(url_for('user', name=userName)) # Redirect the user to the 'user' route and pass the username as a parameter
        else:
            flash("Email is already in use. Please enter a different email.")
            return redirect(url_for('signup')) # If the email is already in use, redirect the user back to the signup page
    return render_template("signup.html", form=form)  # Render the signup.html template with the form



# Create a form class
class SignInForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email(), Length(min=6, max=30)])  # Text input field for email address
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=30)]) # Password input field for password
    submit = SubmitField("Sign in!")  # Submit button for the form


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        # If the form is submitted and passes validation
        email = form.email.data  # Get the email address from the form
        password = form.password.data # Get the password from the form
        
        # Perform user authentication and set the user's login state
        # Example: Check if the email and password are valid
        
        # Assuming the authentication is successful
        user = Users.query.filter_by(email=email).first()    # Query the database for a user with the provided email address
        if user and user.password == password:   # If a user with the email address is found and the password matches
            login_user(user)# Start the session for the user
            flash("Sign IN Submitted Successfully!")
            return redirect(url_for('user', name=email))  # Redirect with the email parameter
         # Redirect the user to the 'user' route and pass the email address as a parameter
        else:
            flash("Invalid email or password. Please try again.")
            return redirect(url_for('signin'))
            # If the email or password is invalid, redirect the user back to the signin page
    return render_template("signin.html", form=form)
        # Render the signin.html template with the form

class ContactForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    cemail = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])# Text input field for full name
    cemail = StringField('Email', validators=[DataRequired(), Email()]) # Text input field for email address
    message = TextAreaField('Message', validators=[DataRequired()]) # Text area field for message
    submit = SubmitField('Submit') # Submit button for the form


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm() # Create an instance of the ContactForm

    if form.validate_on_submit(): # If the form is submitted and passes validation
        full_name = form.full_name.data # Get the full name from the form
        cemail = form.cemail.data # Get the email address from the form
        message = form.message.data # Get the message from the form
 
        # Process the form data here (e.g., send an email)
        # You can add your own code to handle form data (e.g., send an email)
        # Here's a simple example of printing the form data
        print(f"Full Name: {full_name}")
        print(f"Email: {cemail}")
        print(f"Message: {message}")

        flash("Thank you for your message! We will get back to you soon!")
        return redirect(url_for('contact')) # Redirect the user back to the contact page

    return render_template('contact.html', form=form)# Render the contact.html template with the form

@app.route('/faq')
def faq():
    return render_template('faq.html')
#This code defines a route /faq that renders the faq.html template. When a user visits the /faq URL, the template will be rendered and sent back as the response.




class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[InputRequired()]) # Text input field for product name
    product_type = StringField('Product Type', validators=[InputRequired()])   # Text input field for product type
    product_object = StringField('Product Object', validators=[InputRequired()]) # Text input field for product object
    rating_choices = [
        ('poor', 'Poor'),
        ('bad', 'Bad'),
        ('average', 'Average'),
        ('good', 'Good'),
        ('excellent', 'Excellent')
    ]
    rating = SelectField('Rating', choices=rating_choices, validators=[InputRequired()]) # Select field for rating
    comment = StringField('Comment')# Text input field for comment
    image_url = StringField('Image URL' )  # Text input field for image URL
    submit = SubmitField('Submit') # Submit button for the form
    

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

    form = ProductForm() # Create an instance of the ProductForm

    if form.validate_on_submit():   # If the form is submitted and passes validation
        product_name = form.product_name.data # Get the product name from the form
        product_type = form.product_type.data  # Get the product type from the form
        product_object = form.product_object.data # Get the product object from the form
        rating = form.rating.data # Get the rating from the form
        comment = form.comment.data # Get the comment from the form
        image_url = form.image_url.data # Get the image URL from the form

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
        return redirect(url_for('dashboard'))# Redirect the user back to the dashboard page

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
    rating = SelectField('Rating', choices=rating_choices, validators=[InputRequired()])# Select field for rating
    comment = TextAreaField('Comment', validators=[InputRequired(), Length(max=500)])# Text area field for comment
    product_name = StringField('Product Name', validators=[InputRequired()])# Text input field for product name
    product_type = StringField('Product Type', validators=[InputRequired()]) # Text input field for product type
    product_object = StringField('Product Object', validators=[InputRequired()]) # Text input field for product object
    image_url = StringField('Image URL')# Text input field for image URL
    submit = SubmitField('Update')# Submit button for the form

@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)# Get the review with the given review_id from the database
    form = EditReviewForm(obj=review)# Create an instance of EditReviewForm and populate it with the review data

    if form.validate_on_submit():
        form.populate_obj(review)# Update the review object with the form data
        db.session.commit()# Commit the changes to the database
        flash('Review updated successfully!', 'success')# Display a success flash message
        return redirect(url_for('dashboard')) # Redirect the user back to the dashboard

    return render_template('edit_review.html', form=form, review=review)


@app.route('/delete-review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)# Get the review with the given review_id from the database
    
    # Retrieve the associated product
    product = review.product

    # Delete the review and the associated product
    db.session.delete(review)
    db.session.delete(product)

    db.session.commit()
    flash("Review and associated product deleted successfully!")# Display a success flash message
    return redirect(url_for('dashboard'))# Redirect the user back to the dashboard


@app.route('/products', methods=['GET'])
def all_products():
    page = request.args.get('page', 1, type=int)# Get the value of the 'page' query parameter from the URL
    per_page = 4 # Number of products to display per page
    products = Product.query.paginate(page=page, per_page=per_page)# Paginate the products query

    pagination = Pagination(page=page, per_page=per_page, total=products.total, css_framework='bootstrap4') # Create a Pagination object
#A Pagination object is created using Pagination(page=page, per_page=per_page, total=products.total, css_framework='bootstrap4'). This object contains information about the pagination, such as the current page, total number of products, and the CSS framework to use for rendering the pagination links
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
"""
This code defines a route /logout that handles POST requests. When a POST request is made to this route, the code performs the logout process. It calls logout_user() to log out the current user, flashes a success message using flash("Logged out successfully!"), and redirects the user to the 'index' page using redirect(url_for('index')).

If the request method is not POST, the code returns a 405 error (Method Not Allowed) using abort(405). This means that non-POST requests to this route are not allowed.
"""
#create admin panel




@app.route('/admin/login', methods=['GET', 'POST'])

def admin_login():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verify the admin credentials
        if username == 'admin' and check_password_hash(generate_password_hash('admin_password'), password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            error_message = 'Invalid admin credentials. Please try again.'

    return render_template('admin_login.html', error_message=error_message)

"""
This code defines a route /admin/login that handles both GET and POST requests. When a GET request is made, the code renders the admin_login.html template, passing error_message as None.

When a POST request is made, the code retrieves the values of the username and password fields from the form submitted by the user. It then verifies the admin credentials. If the entered username is 'admin' and the entered password matches the password hash generated from 'admin_password', the user is considered authenticated. In this case, the code sets session['admin_logged_in'] to True and redirects the user to the admin_panel route. If the admin credentials are invalid, an error message is set and passed to the admin_login.html template for rendering.
"""

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function
'''
This code defines a decorator function admin_login_required, which is used to protect routes that require admin authentication. It checks whether the admin_logged_in key is present in the session. If it is not present or its value is False, the user is redirected to the admin_login route. If the user is authenticated as an admin, the original route function specified by f is called with the provided arguments and keyword arguments.
'''
@app.route('/admin/panel')
@admin_login_required
def admin_panel():
    users = Users.query.all()
    products = Product.query.all()
    reviews = Review.query.all()
    return render_template('admin_panel.html', users=users, products=products, reviews=reviews)
'''
This code defines a route /admin/panel that requires admin authentication. If the user is authenticated, it retrieves all users, products, and reviews from the database and renders the admin_panel.html template, passing the retrieved data as variables.
'''
@app.route('/admin/delete/user/<int:user_id>', methods=['POST'])
@admin_login_required
def delete_user(user_id):
    user = Users.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete/product/<int:product_id>', methods=['POST'])
@admin_login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete/review/<int:review_id>', methods=['POST'])
@admin_login_required
def deleting_review(review_id):
    review = Review.query.get(review_id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('admin_panel'))
'''
These three code blocks define routes for deleting users, products, and reviews respectively. Each route requires admin authentication. If the user is authenticated, it retrieves the corresponding user, product, or review from the database using the provided user_id, product_id, or review_id. It then deletes the retrieved object from the database and commits the changes. Finally, it redirects the user back to the admin_panel route.
'''
if __name__ == "__main__":
    #The if __name__ == "__main__": block at the end of the code starts the Flask application in debug mode if the script is executed directly.
    app.run(debug=True)
    

