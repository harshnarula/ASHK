from managment import app , db , encode
from datetime import datetime , date
import secrets
import os
from PIL import Image
from flask import render_template , url_for , flash , redirect , request
from managment.form import redistrationform , loginform , Accountform ,tourform ,reviewform
from managment.datbase import User , Tour , Review
from flask_login import login_user , current_user , logout_user , login_required


@app.route('/home')
@app.route('/')
def home():
    rev = Review.query.all()
    user = User
    if current_user.is_authenticated:
        tour = Tour
        image_file = url_for('static' , filename = 'pp/' + current_user.image_file)
        return render_template('home_page.html' , image_file= image_file , rev = rev  , user = user , tour = tour)
    return render_template('home_page.html',rev = rev , user = user )


@app.route('/registration',methods=['GET', 'POST'])
def regi():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = redistrationform()
    if form.validate_on_submit():
        encoded_pass = encode.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first = form.fn.data ,middle = form.mn.data , last = form.ln.data , email = form.email.data , user_type = form.user_type.data , password=encoded_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.fn.data}','success')
        return redirect(url_for('login'))
    return render_template('registration.html' , form=form)





@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and encode.check_password_hash(user.password, form.password.data):
            login_user(user , remember= form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful , Please check the email and Password','danger')
    return render_template('login_page.html' , form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))





def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path , 'static/pp' , picture_fn)
    outout_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(outout_size)
    i.save(picture_path)
    return picture_fn




@app.route('/account' ,methods=['GET', 'POST'])
@login_required
def account():
    form = Accountform()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first = form.fn.data
        current_user.middle = form.mn.data
        current_user.last = form.ln.data
        current_user.email = form.email.data
        current_user.add1 = form.add1.data
        current_user.add2 = form.add2.data
        current_user.add3 = form.add3.data
        current_user.add4 = form.add4.data
        current_user.state = form.add5.data
        current_user.city = form.add6.data
        current_user.pincode = form.pincode.data
        db.session.commit()
        flash("Your Account is Updated!", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.fn.data = current_user.first
        form.mn.data = current_user.middle
        form.ln.data = current_user.last
        form.email.data = current_user.email
        form.add1.data = current_user.add1
        form.add2.data = current_user.add2
        form.add3.data = current_user.add3
        form.add4.data = current_user.add4
        form.add5.data = current_user.state
        form.add6.data = current_user.city
        form.pincode.data = current_user.pincode
    image_file = url_for('static' , filename = 'pp/' + current_user.image_file)
    return render_template('account.html' ,  image_file = image_file , form = form)





@app.route('/plantour' , methods=[ 'GET', 'POST'])
@login_required
def tour():
    form = tourform()
    if form.validate_on_submit():
        ptour = Tour(place = form.place.data , doj = form.doj.data , total_amt = form.total_amt.data , package_amt = form.package_amt.data , nop = form.nop.data , traveler = current_user)
        db.session.add(ptour)
        db.session.commit()
        flash('Your trip is Booked')
    return render_template('tour.html' ,  form = form)



@app.route('/review' , methods=[ 'GET', 'POST'] )
@login_required
def review():
    d = date.today()
    form = reviewform()
    if form.validate_on_submit():
        rev = Review(title = form.title.data , review = form.review.data ,date_review = d , rver = current_user.id)
        db.session.add(rev)
        db.session.commit()
        flash( 'Review is created' , 'success' )
        return redirect(url_for('home'))
    return render_template('review.html' ,  form = form)
