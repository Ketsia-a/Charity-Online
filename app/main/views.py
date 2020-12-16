from flask import render_template,request,redirect,url_for,abort,current_app
from ..models import User,Event
from . import main
from flask_login import login_required
from .. import db,photos
from .forms import EventForm
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

                new_event = Event(description=description,user_id=current_user._get_current_object().id,event_pic_path=event_pic_path,category=category,title=title)
                db.session.add(new_event)
                db.session.commit()
        
            return redirect(url_for('main.index'))
        else:
            event_pic_path = 'https://www.freevector.com/uploads/vector/preview/25765/Charity_-01.jpg'    
            if form.validate_on_submit():

                new_event = Event(description=description,user_id=current_user._get_current_object().id,event_pic_path=event_pic_path,category=category,title=title)
                db.session.add(new_event)
                db.session.commit()
        
            return redirect(url_for('main.index'))

        
    return render_template('event.html', form = form)