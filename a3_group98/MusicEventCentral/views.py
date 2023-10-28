from flask import Blueprint, render_template
from .models import Event
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events=events)


# @mainbp.route('/search')
# def search():
#     if request.args['search'] and request.args['search'] != "":
#         print(request.args['search'])
#         query = "%" + request.args['search'] + "%"
#         destinations = db.session.scalars(db.select(Destination)).where(
#             Destination.description.like(query))
#         return render_template('index.html', destinations=destinations)
#     else:
#         return redirect(url_for('main.index'))
