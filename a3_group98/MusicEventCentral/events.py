from flask import Blueprint, render_template, request, redirect, url_for
# from .models import Event
from .forms import EventForm


evtbp = Blueprint('event', __name__, url_prefix='/events')


@evtbp.route('/listing')
def listing():
    return render_template('events/event_listing.html')


@evtbp.route('/create', methods=['GET', 'POST'])
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        print('Successfully created new event')
        return redirect(url_for('event.create'))
    return render_template('events/event_creation.html', form=form)

# @evtbp.route('/create')
# def create():
#     return render_template('events/event_creation.html')


@evtbp.route('/details')
def details():
    return render_template('events/event_details.html')
