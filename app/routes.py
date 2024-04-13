from app import app, db
from flask import render_template, request, session, redirect, url_for, flash, get_flashed_messages
from app.models import User

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            error_message = 'Missing username, email, or password'
            return render_template('register.html', error_message=error_message)

        if User.find_by_username(username):
            error_message = 'Username already exists'
            return render_template('register.html', error_message=error_message)

        if User.find_by_email(email):
            error_message = 'Email already registered'
            return render_template('register.html', error_message=error_message)

        # If no validation errors, proceed with user registration
        user = User(username=username, email=email, password=password)
        user.save()

        success_message = 'User registered successfully'
        return render_template('login.html', success_message=success_message)

    # Render the empty register.html template for GET requests
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        # User is already logged in, redirect to another page (e.g., index)
        flash('You are already logged in.', 'info')
        return redirect(url_for('index'))
    
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            error_message = 'Missing email or password'
            return render_template('login.html', error_message=error_message)

        user = User.find_by_email(email)

        if not user:
            print(f"No user found for email: {email}")
            error_message = 'Invalid email or password'
            return render_template('login.html', error_message=error_message)
        
        session['email'] = email # Store email in session for authentication


        # Flash a success message
        flash('Logged in successfully!', 'success')

        # Redirect to index page after successful login
        return redirect(url_for('index'))

        # success_message = 'User logged in successfully'
        # return render_template('index.html', success_message=success_message)

    return render_template('login.html')



@app.route('/logout', methods=['POST'])
def logout():
    # Clear session data
    session.pop('email', None)

    # Flash a logout message

    flash('Logged out successfully!', 'success')
    response = redirect(url_for('login'))
    
    response.delete_cookie('session')
    response.delete_cookie('email')
    
    # Redirect to the login page
    return response




@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Check if user is logged in (email exists in session)
    if 'email' in session:
        email = session['email']
        user = User.find_by_email(email)
        if user:
            # Store user data in local storage for client-side access
            user_data = {
                'email': user.email,
                'username': user.username
            }
            # Get flashed messages and render index template with user data and messages
            messages = [msg for msg in get_flashed_messages()]
            return render_template('dashboard.html', user_data=user_data, messages=messages)

    # If user is not logged in, redirect to login page
    return redirect(url_for('login'))



@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if user is logged in (email exists in session)
    if 'email' in session:
        email = session['email']
        user = User.find_by_email(email)
        if user:
            # Store user data in local storage for client-side access
            user_data = {
                'email': user.email,
                'username': user.username
            }
            # Get flashed messages and render index template with user data and messages
            messages = [msg for msg in get_flashed_messages()]
            return render_template('index.html', user_data=user_data, messages=messages)

    # If user is not logged in, redirect to login page
    return render_template('index.html')



@app.route('/about', methods=['GET', 'POST'])
def about():
    # Check if user is logged in (email exists in session)
    if 'email' in session:
        email = session['email']
        user = User.find_by_email(email)
        if user:
            # Store user data in local storage for client-side access
            user_data = {
                'email': user.email,
                'username': user.username
            }
            # Get flashed messages and render index template with user data and messages
            messages = [msg for msg in get_flashed_messages()]
            return render_template('about.html', user_data=user_data, messages=messages)

    # If user is not logged in, redirect to login page
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # Check if user is logged in (email exists in session)
    if 'email' in session:
        email = session['email']
        user = User.find_by_email(email)
        if user:
            # Store user data in local storage for client-side access
            user_data = {
                'email': user.email,
                'username': user.username
            }
            # Get flashed messages and render index template with user data and messages
            messages = [msg for msg in get_flashed_messages()]
            return render_template('contact.html', user_data=user_data, messages=messages)

    # If user is not logged in, redirect to login page
    return render_template('contact.html')

