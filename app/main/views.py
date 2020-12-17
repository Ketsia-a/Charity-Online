from flask import render_template,request,redirect,url_for,abort,current_app
from ..models import User,Event,Donor
from . import main
from flask_login import login_required
from .. import db,photos
from .forms import EventForm,DonorForm
from flask_login import current_user

# Views
@main.route('/')
def index():
    event = Event.query.order_by(Event.time.desc()).all()
    food = Event.query.filter_by(category = 'Food').order_by(Event.time.desc()).all() 
    clothes = Event.query.filter_by(category = 'Clothes').order_by(Event.time.desc()).all()
    money = Event.query.filter_by(category = 'Money').order_by(Event.time.desc()).all()
    books = Event.query.filter_by(category = 'Books').order_by(Event.time.desc()).all()
    title ='Charity'
    return render_template('index.html', food = food, clothes = clothes, money = money, books= books, title=title, event=event)

@main.route('/new_event', methods = ['POST','GET'])
@login_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        category = form.category.data
        value = form.value.data
        user_id = current_user
        if form.event_pic_path.data:
            event_pic_path = form.event_pic_path.data     
            if form.validate_on_submit():

                new_event = Event(description=description,user_id=current_user._get_current_object().id,event_pic_path=event_pic_path,category=category,value=value,title=title)
                db.session.add(new_event)
                db.session.commit()
        
            return redirect(url_for('main.index'))
        else:
            event_pic_path = 'https://www.freevector.com/uploads/vector/preview/25765/Charity_-01.jpg'    
            if form.validate_on_submit():

                new_event = Event(description=description,user_id=current_user._get_current_object().id,event_pic_path=event_pic_path,category=category,title=title,value=value)
                db.session.add(new_event)
                db.session.commit()
        
            return redirect(url_for('main.index'))

        
    return render_template('event.html', form = form)



@main.route('/donor/<int:event_id>', methods = ['POST','GET'])
def donor(event_id):
    form = DonorForm()
    event = Event.query.get(event_id)
    all_donors = Donor.query.filter_by(event_id = event_id).all()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        amount = form.value.data
        event_id = event_id
        new_donor = Donor(name = name, email = email, amount = amount,event_id = event_id)
        
        db.session.add(new_donor)
        db.session.commit()
        return redirect(url_for('.index', event_id = event_id))
    return render_template('donation.html', form =form, event = event,all_donors=all_donors) 

@main.route('/index/<int:id>/delete',methods = ['GET','POST'])
@login_required
def delete(id):
    current_event = Event.query.filter_by(id = id).first()
    if current_event.user != current_user:
        abort(404)
    db.session.delete(current_event)
    db.session.commit()

    return redirect(url_for('.index'))    