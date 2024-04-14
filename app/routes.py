from app import app, db
from flask import render_template, request, session, redirect, url_for, flash, get_flashed_messages
from app.models import Project, User, Feedback, Task

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
            
            email = session.get('email')
    
            user_id = User.find_user_id(email)
            projects = Project.find_by_user(user_id)
            
            # Get flashed messages and render index template with user data and messages
            messages = [msg for msg in get_flashed_messages()]
            return render_template('dashboard.html', user_data=user_data, messages=messages, projects=projects)

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
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        subject = request.form['subject']
        message = request.form['message']
        
        # If no validation errors, proceed with user registration
        feedback = Feedback(fullname=fullname, email=email, phonenumber=phonenumber, subject=subject, message=message)
        feedback.save()

        success_message = 'Feedback sent successfully'
        return render_template('contact.html', success_message=success_message)
            
    return render_template('contact.html')



@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    if 'admin-email' in session:
        # User is already logged in, redirect to another page (e.g., index)
        flash('You are already logged in.', 'info')
        return redirect(url_for('adminDashboard'))
    
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']


        if not email or not password:
            error_message = 'Missing email or password'
            return render_template('login.html', error_message=error_message)

        user = User.find_by_email(email)
        print(f"User details - Username: {user.username}, Email: {user.email}, UserType: {user.usertype}")

        
        if user.usertype != "Admin":
            print(f"No Admin found for email: {email}")
            error_message = 'Invalid email or password'
            return render_template('adminLogin.html', error_message=error_message)
        
        session['admin-email'] = email # Store email in session for authentication


        # Flash a success message
        flash('Logged in successfully!', 'success')

        # Redirect to index page after successful login
        return redirect(url_for('adminDashboard'))
    
    return render_template('adminLogin.html')



@app.route('/adminDashboard', methods=['GET', 'POST'])
def adminDashboard():
    # Check if user is logged in (email exists in session)
    if 'admin-email' in session:
        email = session['admin-email']
        user = User.find_by_email(email)
        if user:
            # Store user data in local storage for client-side access
            user_data = {  
                'email': user.email,
                'username': user.username
            }
            
            
            feedbacks = list(Feedback.find_all_feedback())
            users = list(User.find_all_users())
            numberofuser = len(users)
            numberoffeedback = len(feedbacks)
            
            
            # Get flashed messages and render index template with user data and messages
            messages = [msg for msg in get_flashed_messages()]
            return render_template('adminDashboard.html', user_data=user_data, users=users, numberofuser=numberofuser, numberoffeedback=numberoffeedback, feedbacks= feedbacks, messages=messages)

    # If user is not logged in, redirect to login page
    return redirect(url_for('login'))




@app.route('/adminLogout', methods=['POST'])
def adminLogout():
    # Clear session data
    session.pop('admin-email', None)

    # Flash a logout message

    flash('Logged out successfully!', 'success')
    response = redirect(url_for('adminLogin'))
    
    response.delete_cookie('session')
    response.delete_cookie('admin-email')
    
    # Redirect to the login page
    return response


@app.route('/deleteUser', methods=['POST'])
def deleteUser():
    
    user_id = request.form.get('user_id')
    
    deleted_count = User.delete_by_id(user_id)  # Delete user by ID
    if deleted_count == 0:
        error_message = 'User not found'
        return render_template('adminDashboard.html', error_message=error_message)
    
    flash('User deleted successfully!', 'success')
    response = redirect(url_for('adminDashboard'))
    return response


@app.route('/deleteFeedback', methods=['POST'])
def deleteFeedback():
    
    feedback_id = request.form.get('feedback_id')
    
    deleted_count = Feedback.delete_by_id(feedback_id)  # Delete user by ID
    if deleted_count == 0:
        error_message = 'Feedback not found'
        return render_template('adminDashboard.html', error_message=error_message)
    
    flash('Feedback deleted successfully!', 'success')
    response = redirect(url_for('adminDashboard'))
    return response


@app.route('/createProject', methods=['POST'])
def createProject():
    # Extract project details from request
    
    email = session.get('email')
    print(email)
    
    userid = User.find_user_id(email)
    projecttitle = request.form['projecttitle']
    projectdescription = request.form['projectdescription']
    
    # Create a new Project object
    project = Project(userid=userid, projecttitle=projecttitle, projectdescription=projectdescription)
    # Save the project to the database
    project.save()
    
    flash('Project created successfully'
, 'success')
    response = redirect(url_for('dashboard'))
    return response


@app.route('/singleProject/<project_id>', methods=['GET'])
def singleProject(project_id):
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
    
            project = Project.find_project_by_id(project_id)
            # Get flashed messages and render index template with user data and messages
            messages = [msg for msg in get_flashed_messages()]
            return render_template('singleProject.html', project=project,  user_data=user_data, messages=messages)

    # If user is not logged in, redirect to login page
    return redirect(url_for('login'))




@app.route('/addTodoTask', methods=['POST'])
def addTodoTask():
    if request.method == 'POST':
        request_data = request.get_json()

        projectid = request_data.get('projectid')  # Retrieve project ID from AJAX request
        tasktitle = request_data.get('tasktitle')  # Retrieve task title from AJAX request
        taskstatus = request_data.get('taskstatus')  # Retrieve task status from AJAX request
    
        print(projectid, tasktitle)
    
        # Create a new Project object
        task = Task(projectid=projectid, tasktitle=tasktitle, taskstatus=taskstatus)
        # Save the project to the database
        task.save()
    
        flash('Task added successfully', 'success')
        response = redirect(url_for('dashboard'))
        return response


@app.route('/deleteProject', methods=['POST'])
def deleteProject():
    
    projectid = request.form.get('projectid')
    
    deleted_count = Project.delete_project_by_id(projectid)  # Delete user by ID
    if deleted_count == 0:
        error_message = 'Feedback not found'
        return render_template('dashboard.html', error_message=error_message)
    
    flash('Project deleted successfully!', 'success')
    response = redirect(url_for('dashboard'))
    return response



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
