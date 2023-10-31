from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db
from datetime import datetime

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()

    for event in events:
        update_status(event.id)

    return render_template('index.html', events=events)


def update_status(id):
    events = db.session.scalar(db.select(Event).where(Event.id == id))
    if events.end_date < datetime.now().date():
        print("inactive")
        events.status = "Inactive"
        db.session.commit()

    if events.tickets_avail < 1:
        events.status = "Sold Out"
        db.session.commit()


# Search route. Search bar in header (in base.html).
@bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(
            db.select(Event).where((Event.name.like(query)) | (Event.genre.like(query) | (Event.start_date.like(query)))))
        return render_template('events/event_listing.html', events=events)
    else:
        return redirect(url_for('main.base'))
