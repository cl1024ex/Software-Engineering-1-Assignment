"""
Route.py
This file is where the routing takes place.
It contains all the route definitions for the application,
including user authentication, attraction management, review management,
and admin functionalities. This is the central file that connects the frontend
templates with the backend logic and database operations defined in the __init__.py file.

"""

from application import app
from flask import render_template, request, redirect, flash, url_for, session
from application.models import User, Admin, Attractions, Reviews
from application.forms import LoginForm, RegisterForm
from werkzeug.utils import secure_filename
import os


def get_next_available_review_id():
    """
    This function generates the next available review ID by checking existing
    review IDs in the database. It retrieves all existing review IDs, and then
    iterates through the range of possible IDs to find the smallest missing ID.
    If there are no existing reviews, it returns 1 as the next available ID.
    This ensures that review IDs are unique and sequential, even if some reviews
    have been deleted.
    """
    existing_ids = [r.reviewID for r in Reviews.objects.order_by('reviewID')]

    if not existing_ids:
        return 1

    for i in range(1, max(existing_ids) + 2):
        if i not in existing_ids:
            return i

    return max(existing_ids) + 1


def get_next_available_attraction_id():
    """
    This function generates the next available attraction ID by checking existing
    attraction IDs in the database. It retrieves all existing attraction IDs, and then
    iterates through the range of possible IDs to find the smallest missing ID.
    If there are no existing attractions, it returns 1 as the next available ID.
    This ensures that attraction IDs are unique and sequential, even if some attractions
    have been deleted.
    """
    existing_ids = [r.attractionID for r in Attractions.objects.order_by('attractionID')]

    if not existing_ids:
        return 1

    for i in range(1, max(existing_ids) + 2):
        if i not in existing_ids:
            return i

    return max(existing_ids) + 1


def get_next_available_user_id():
    """
    This function generates the next available user ID by checking existing
    user IDs in the database. It retrieves all existing user IDs, and then
    iterates through the range of possible IDs to find the smallest missing ID.
    If there are no existing users, it returns 1 as the next available ID.
    This ensures that user IDs are unique and sequential, even if some users
    have been deleted.
    """
    existing_ids = [r.user_id for r in User.objects.order_by('user_id')]

    if not existing_ids:
        return 1

    for i in range(1, max(existing_ids) + 2):
        if i not in existing_ids:
            return i

    return max(existing_ids) + 1


def get_next_available_admin_id():
    """
    This function generates the next available admin ID by checking existing
    admin IDs in the database. It retrieves all existing admin IDs, and then
    iterates through the range of possible IDs to find the smallest missing ID.
    If there are no existing admins, it returns 1 as the next available ID.
    This ensures that admin IDs are unique and sequential, even if some admins
    have been deleted.
    """
    existing_ids = [r.adminID for r in Admin.objects.order_by('adminID')]

    if not existing_ids:
        return 1

    for i in range(1, max(existing_ids) + 2):
        if i not in existing_ids:
            return i

    return max(existing_ids) + 1


@app.route("/home")
def home():
    """
    This is the home route
    URL endpoint: /home
    Methods: GET
    Description: Renders the home page template. This is the default landing page
    for the application. This is the default landing page for the application
    """
    return render_template("home.html", home=True)


def register():
    """
    This is the registration route
    URL endpoint: /register
    Methods: GET, POST
    Description: Handles user registration
    On GET request, it renders the registration form
    On POST request, it processes the form data, creates a new user,
    and saves it to the database. After successful registration, it
    redirects the user to the home page if not successful error message flashed 
    and stay on the registration page.
    """
    if session.get('username'):
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        user_id = get_next_available_user_id()
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        flash("You are registered","success")
        return redirect(url_for('home'))

    return render_template("register.html", title="Register", form=form, register=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    This is the login route
    URL endpoint: /login
    Methods: GET, POST
    Description: Handles user login
    On GET request, it renders the login form
    On POST request, it processes the form data, checks the user's credentials,
    and if valid, logs the user in by setting session variables. After
    successful login, it redirects the user to the home page. If the
    credentials are invalid, it flashes an error message. If the user is
    an admin, it also sets an "is_admin" flag in the session for admin-specific
    functionalities.
    """
    if session.get('username'):
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name} , You are successfully logged in", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            session['is_admin'] = Admin.objects(user_id=user.user_id).first() is not None
            return redirect(url_for('home'))
        else:
            flash("Sorry, try again","danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/logout")
def logout():
    """
    This is the logout route
    URL endpoint: /logout
    Methods: GET
    Description: Logs the user out by clearing the session variables and
    redirects to the home page
    """
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return redirect(url_for('home'))


@app.route("/browse")
def browse():
    """
    This is the browse route
    URL endpoint: /browse
    Methods: GET
    Description: Renders the browse page with a list of approved attractions.
    It also supports searching for attractions by name using a query parameter.
    If a search query is provided, it filters the attractions to only include
    those.
    """
    search_query = request.args.get('search', '').strip()
    if search_query:
        attractions = Attractions.objects(status="approved", name__icontains=search_query)
    else:
        attractions = Attractions.objects(status="approved")
    return render_template("browse.html", attractions=attractions)


@app.route("/user")
def user():
    """
    This is the user route.
    URL endpoint: /user
    Methods: GET
    Description: Renders the user page with a list of all users.
    This page is typically used by admins to manage users. It retrieves
    all user records from the database and passes them to the template for
    display
    """
    users = User.objects.all()
    return render_template("users.html", users=users)


@app.route("/attraction/<int:attraction_id>")
def attraction_detail(attraction_id):
    """
    This is the attraction detail route
    URL endpoint: /attraction/<int:attraction_id>
    Methods: GET
    Parameters: attraction_id (int) - The ID of the attraction to be displayed
    Description: Renders the attraction detail page for a specific attraction.
    It retrieves the attraction from the database using the provided ID and
    checks if it is approved. It also retrieves all non-reported reviews for
    that attraction. If the attraction is not found or not approved, it flashes
     an error message and redirects back to the browse page. Otherwise, it
     renders the attraction detail template with the attraction and its
     reviews.

    """
    attraction = Attractions.objects(attractionID=attraction_id, status="approved").first()
    reviews = Reviews.objects(attractionID=attraction_id, reported=False)

    return render_template("attraction.html", attraction=attraction, reviews=reviews)


@app.route("/pending_attraction/<int:attraction_id>")
def pending_attraction_detail(attraction_id):
    """
    This is the pending attraction detail route
    URL endpoint: /pending_attraction/<int:attraction_id>
    Methods: GET
    Parameters: attraction_id (int) - The ID of the pending attraction to be
    displayed
    Description: Renders the pending attraction detail page for a specific
    attraction.This page is typically used by admins to review pending
    attractions. It retrieves the attraction from the database using the
    provided ID and checks if it is pending. It also retrieves all reviews
    for that attraction, regardless of their reported status. If the attraction
    is not found or not pending, it flashes an error message and redirects
    back to the admin page. Otherwise, it renders the pending attraction
    detail template with the attraction and its reviews for admin review
    and approval.
    """
    attraction = Attractions.objects(attractionID=attraction_id).first()
    if not attraction:
        flash("Attraction not found", "danger")
        return redirect(url_for('admin'))
    reviews = Reviews.objects(attractionID=attraction_id)

    return render_template("pending_attraction_detail.html", attraction=attraction, reviews=reviews)

@app.route("/my_pending")
def my_pending():
    """
    This is the my pending attractions route
    URL endpoint: /my_pending
    Methods: GET
    Description: Renders the page with a list of the current user's pending attractions.
    This page is used by users to view and manage their own pending attractions. It checks
    if the user is logged in, and if so, retrieves all attractions created by the user that
    are not approved. If the user is not logged in, it flashes a warning message and redirects
    to the login page. Otherwise, it renders the my pending template with the list of pending
    attractions for the user.
    """
    if not session.get('user_id'):
        flash("Please log in to view your pending attractions", "warning")
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    pending_attractions = Attractions.objects(created_by=user_id, status__ne="approved")
    return render_template("my_pending.html", pending_attractions=pending_attractions, pending=True)


@app.route("/add_attraction", methods=["GET", "POST"])
def add_attraction():
    """
    This is the add attraction route
    URL endpoint: /add_attraction
    Methods: GET, POST
    Description: Handles adding a new attraction. On GET request, it renders
    the add attraction form. On POST request, it processes the form data, creates
    a new attraction object, and saves it to the database. The attraction is initially
    set to "pending" status and is associated with the current user. After successful 
    creation, it flashes a success message and redirects to the browse page. If the user
    is not logged in, it flashes a warning message and redirects to the login page.
    """
    if request.method == "POST":
        attractionID = get_next_available_attraction_id()
        attractionID = str(attractionID)
        name = request.form.get("attraction_name")
        description = request.form.get("description")
        location = request.form.get("location")
        image_file = request.files.get('image')
        image_field = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            images_dir = os.path.join(app.root_path, 'static', 'images')
            os.makedirs(images_dir, exist_ok=True)
            save_path = os.path.join(images_dir, filename)
            image_file.save(save_path)
            image_field = f"images/{filename}"

        status = "pending"
        created_by = session.get('user_id')

        attraction = Attractions(attractionID=attractionID, name=name, description=description, location=location, image=image_field, status=status, created_by=created_by)
        attraction.save()

        flash(f"{name} has been added and is pending approval", "success")
        return redirect(url_for('browse'))

    return render_template("add_attraction.html", title="Add Attraction")


@app.route("/edit_attraction/<int:attraction_id>", methods=["GET", "POST"])
def edit_attraction(attraction_id):
    """
    This is the edit attraction route.
    URL endpoint: /edit_attraction/<int:attraction_id>
    Methods: GET, POST
    Parameters: attraction_id (int) - The ID of the attraction to be edited.
    Description: Handles editing an existing attraction. On GET request, it
    renders the edit form with the current attraction details. On POST request,
    it processes the form data, updates the attraction in the database, and saves
    the changes. Only the creator of the attraction can edit it, and only if the
    attraction is still pending or rejected. After successful editing, it flashes
    a success message and redirects back to the user's pending attractions page. If
    the attraction is not found, the user does not have permission, or the attraction
    is not pending/rejected, it flashes an appropriate error message and redirects back
    to the user's pending attractions page.                            
    """
    attraction = Attractions.objects(attractionID=attraction_id).first()
    if not attraction:
        flash("Attraction not found", "danger")
        return redirect(url_for('my_pending'))

    if attraction.created_by != session.get('user_id'):
        flash("You do not have permission to edit this attraction", "danger")
        return redirect(url_for('my_pending'))

    if attraction.status not in ["pending", "rejected"]:
        flash("You can only edit pending or rejected attractions", "warning")
        return redirect(url_for('my_pending'))

    if request.method == "POST":
        attraction.name = request.form.get("attraction_name")
        attraction.description = request.form.get("description")
        attraction.location = request.form.get("location")

        image_file = request.files.get('image')
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            images_dir = os.path.join(app.root_path, 'static', 'images')
            os.makedirs(images_dir, exist_ok=True)
            save_path = os.path.join(images_dir, filename)
            image_file.save(save_path)
            attraction.image = f"images/{filename}"

        if attraction.status == "rejected":
            attraction.status = "pending"

        attraction.save()
        flash("Attraction updated successfully!", "success")
        return redirect(url_for('my_pending'))

    return render_template("edit_attraction.html", attraction=attraction)


@app.route("/delete_attraction/<int:attraction_id>", methods=["POST"])
def delete_attraction(attraction_id):
    """
    This is the delete attraction route
    URL endpoint: /delete_attraction/<int:attraction_id>
    Methods: POST
    Parameters: attraction_id (int) - The ID of the attraction to be deleted.
    Description: Deletes an attraction from the database. This route is typically
    used by users to delete their own pending attractions. It takes the attraction
    ID as a parameter, checks if the attraction exists and if the current user is the
    creator of the attraction. If both conditions are met and the attraction is still
    pending, it deletes the attraction from the database. After deletion, it flashes a
    success message and redirects back to the user's pending attractions page. If the
    attraction is not found, the user does not have permission, or the attraction is
    not pending, it flashes an appropriate error message and redirects back to the user's
    pending attractions page.
    """
    attraction = Attractions.objects(attractionID=attraction_id).first()
    if not attraction:
        flash("Attraction not found", "danger")
        return redirect(url_for('my_pending'))

    if attraction.created_by != session.get('user_id'):
        flash("You do not have permission to delete this attraction", "danger")
        return redirect(url_for('my_pending'))

    if attraction.status != "pending":
        flash("You can only delete pending attractions", "warning")
        return redirect(url_for('my_pending'))

    attraction.delete()
    flash("Attraction deleted successfully!", "success")
    return redirect(url_for('my_pending'))


@app.route("/add_review/<int:attraction_id>", methods=["GET", "POST"])
def add_review(attraction_id):
    """
    This is the add review route.
    URL endpoint: /add_review/<int:attraction_id>
    Methods: GET, POST
    Parameters: attraction_id (int) - The ID of the attraction to which the review is
    being added.
    Description: Handles adding a review for a specific attraction. On GET request,
    it renders the add review form for the specified attraction. On POST request,
    it processes the form data, creates a new review with a uniqueID, and saves it
    to the database. The review includes the reviewer's name (or "Anonymous" if not
    logged in), rating, review text, and a reported flag set to False. After successfully 
    adding the review, it flashes a success message and redirects the user back to the
    browse page. If the attraction is not found, it flashes an error message and redirects
    back to the browse page.

    """
    attraction = Attractions.objects(attractionID=str(attraction_id)).first()

    if request.method == "POST":
        reviewID = get_next_available_review_id()
        if not session.get('user_id'):
            first_name = request.form.get("name") or "Anonymous"
        else:
            first_name = User.objects(user_id=session['use_id']).first().first_name
        rating = int(request.form.get("rating"))
        review_text = request.form.get("review")
        reported = False

        review = Reviews(reviewID=reviewID, attractionID=attraction_id, first_name=first_name, rating=rating, review=review_text, reported=reported)
        review.save()

        flash("Review added successfully!", "success")
        return redirect(url_for('browse'))

    return render_template("add_review.html", attraction=attraction)


@app.route("/approve_review/<int:review_id>", methods=["POST"])
def approve_review(review_id):
    """
    This is the approve review route.
    URL endpoint: /approve_review/<int:review_id>
    Methods: POST
    Parameters: review_id (int) - The ID of the review to be approved.
    Description: Approves a reported review by changing its status to "approved".
    This route is typically used by admins to approve reviews that have been reported
    as inappropriate but are deemed acceptable. It takes the review ID as a parameter,
    finds the corresponding review in the database, updates its status to "approved",
    and resets the "reported" flag to False. After approval, it flashes a success message 
    and redirects back to the admin page. If the review is not found or has not been
    reported, it flashes an appropriate message and redirects back to the admin page. 
    """
    review = Reviews.objects(reviewID=review_id).first()
    if not review:
        flash("Review not found", "danger")
        return redirect(url_for('admin'))
    if not review.reported:
        flash("Review has not been reported", "warning")
        return redirect(url_for('admin'))
    review.status = "approved"
    review.reported = False
    review.save()
    flash("Review approved", "success")
    return redirect(url_for('admin'))


@app.route("/report_review/<int:review_id>", methods=["POST"])
def report_review(review_id):
    """
    This is the report review route.
    URL endpoint: /report_review/<int:review_id>
    Methods: POST
    Parameters: review_id (int) - The ID of the review to be reported.
    Description: Reports a review as inappropriate. This route is
    typically used by users to flag reviews that they find offensive
    or inappropriate. It takes the review ID as a parameter, finds the
    corresponding review in the database, sets its "reported" flag to
    True, and saves the changes. After reporting, it flashes a warning
    message to the user and redirects back to the previous page. If the
    review is not found, it flashes an error message and redirects back
    to the browse page.  
    """
    review = Reviews.objects(reviewID=review_id).first()
    if not review:
        flash("Review not found", "danger")
        return redirect(url_for('browse'))
    review.reported = True
    review.save()
    flash("Review reported. Admins will review it.", "warning")
    return redirect(request.referrer or url_for('browse'))

@app.route("/reject_review/<int:review_id>", methods=["POST"])
def reject_review(review_id):
    """
    This is the reject review route.
    URL endpoint: /reject_review/<int:review_id>
    Methods: POST
    Parameters: review_id (int) - The ID of the review to be rejected.
    Description: Rejects a reported review by changing its status to "rejected".
    This route is typically used by admins to reject reviews that have been reported
    as inappropriate. It takes the review ID as a parameter, finds the corresponding
    review in the database, updates its status to "rejected", and saves the changes.
    After rejection, it flashes a warning message and redirects back to the admin page.
    If the review is not found or has not been reported, it flashes an appropriate
    message and redirects back to the admin page.
    """
    review = Reviews.objects(reviewID=review_id).first()
    if not review:
        flash("Review not found", "danger")
        return redirect(url_for('admin'))
    if not review.reported:
        flash("Review has not been reported", "warning")
        return redirect(url_for('admin'))
    # delete the review when rejected
    review.status = "rejected"
    review.save()
    flash("Review rejected", "warning")
    return redirect(url_for('admin'))


@app.route("/admin")
def admin():
    """
    This is the admin route.
    URL endpoint: /admin
    Methods: GET
    Description: Renders the admin page with lists of users, pending attractions,
    pending reviews, and admins. This page is only accessible to users with admin
    privileges. It allows admins to manage users, approve or reject attractions,
    and review reported reviews. The route queries the database for all users except
    the current user, all pending attractions, all reported reviews, and all admins.
    It then renders the admin template with this data for display and management.
    """
    current_user_id = session.get('user_id')
    users = User.objects(user_id__ne=current_user_id)
    pending_attractions = Attractions.objects(status="pending")
    pending_reviews = Reviews.objects(reported=True)
    admins = Admin.objects.all()

    reviews_with_attractions = []
    for review in pending_reviews:
        attraction = Attractions.objects(attractionID=str(review.attractionID)).first()
        attraction_name = attraction.name if attraction else "Unknown"
        reviews_with_attractions.append({
            'review': review,
            'attraction_name': attraction_name
        })

    return render_template("admin.html", users=users, pending_attractions=pending_attractions, pending_reviews=reviews_with_attractions, admins=admins)


@app.route("/make_admin/<int:user_id>", methods=["POST"])
def make_admin(user_id):
    """
    This is the make admin route.
    URL endpoint: /make_admin/<int:user_id>
    Methods: POST
    Parameters: user_id (int) - The ID of the user to be granted admin privileges
    Description: Grants admin privileges to a user. This route is typically used
    by existing admins to promote other users to admin status. Then route checks
    if the current user is an admin, and if so, it finds the user by ID and creates
    a new admin record in the database. After granting admin privileges, it flashes
    a success message and redirects back to the admin page. If the user is not found
    or is already an admin, it flashes an appropriate message and redirects back to
    the admin page.   
    """
    if not session.get('is_admin'):
        flash("You are not authorised", "danger")
        return redirect(url_for('home'))
    user = User.objects(user_id=user_id).first()
    if not user:
        flash("User not found", "danger")
        return redirect(url_for('admin'))

    if Admin.objects(user_id=user_id).first():
        flash(f"{user.first_name} is already an admin", "info")
        return redirect(url_for('admin'))

    adminID = get_next_available_admin_id()
    admin_record = Admin(adminID=adminID, user_id=user_id)
    admin_record.save()
    flash(f"{user.first_name} is now an admin", "success")
    return redirect(url_for('admin'))


@app.route("/remove_admin/<int:user_id>", methods=["POST"])
def remove_admin(user_id):
    """
    This is the remove admin route.
    URL endpoint: /remove_admin/<int:user_id>   
    Methods: POST
    Parameters: user_id (int) - The ID of the user to be removed from admin privileges.
    Description: Removes admin privileges from a user.
    This route is typically used by existing admins to revoke admin
    privileges from other users. It takes the user ID as a parameter,
    checks if the user is currently an admin, and if so, deletes the
    corresponding admin record from the database. After removal, it 
    flashes a success message and redirects back to the admin page.
    If the user is not found or is not an admin, it flashes an appropriate
    message and redirects back to the admin page.
    """
    if not session.get('is_admin'):
        flash("You are not authorised", "danger")
        return redirect(url_for('home'))
    admin_record = Admin.objects(user_id=user_id).first()
    if admin_record:
        admin_record.delete()
        user = User.objects(user_id=user_id).first()
        if user:
            flash(f"{user.first_name} is no longer an admin", "success")
    return redirect(url_for('admin'))

@app.route("/approve_attraction/<attraction_id>", methods=["POST"])
def approve_attraction(attraction_id):
    """
    This is the approve attraction route.
    URL endpoint: /approve_attraction/<attraction_id>
    Methods: POST
    Parameters: attraction_id (int) - The ID of the attraction to be approved.
    Description: Approves an attraction by changing its status to "approved".
    This route is typically used by admins to approve attractions that meet the
    approval criteria. It takes the attraction ID as a parameter, finds the 
    corresponding attraction in the database, updates its status to "approved",
    and saves the changes. After approval, it flashes a success message and
    redirects back to the admin page.
    """
    attraction = Attractions.objects(attractionID=attraction_id).first()
    attraction.status = "approved"
    attraction.save()
    flash(f"Attraction '{attraction.name}' approved", "success")
    return redirect(url_for('admin'))


@app.route("/reject_attraction/<attraction_id>", methods=["POST"])
def reject_attraction(attraction_id):
    """
    This is the reject attraction route.
    URL endpoint: /reject_attraction/<attraction_id>
    Methods: POST
    Parameters: attraction_id (int) - The ID of the attraction to be rejected.
    Description: Rejects an attraction by changing its status to "rejected".
    This route is typically used by admins to reject attractions that do not
    meet the approval criteria. It takes the attraction ID as a parameter,
    finds the corresponding attraction in the database, updates its status to
    "rejected", and saves the changes. After rejection, it flashes a warning
    message and redirects back to the admin page.
    """
    attraction = Attractions.objects(attractionID=attraction_id).first()
    attraction.status = "rejected"
    attraction.save()
    flash(f"Attraction '{attraction.name}' rejected", "warning")
    return redirect(url_for('admin'))


@app.route("/delete_review/<int:review_id>", methods=["POST"])
def delete_review(review_id):
    """
    This is the delete review route.
    URL endpoint: /delete_review/<int:review_id> 
    Methods: POST
    Parameters: review_id (int) - The ID of the review to be deleted.
    Description: Deletes a review from the database.
    This route is typically used by admins to remove inappropriate reviews.
    It takes the review ID as a parameter, finds the corresponding review in
    the database, and deletes it. After deletion, it flashes a success message
    and redirects back to the admin page.
    """
    review = Reviews.objects(reviewID=review_id).first()
    if review:
        review.delete()
        flash("Review deleted", "success")
    else:
        flash("Review not found", "danger")
    return redirect(url_for('admin'))
