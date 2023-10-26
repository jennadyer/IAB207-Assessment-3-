from MusicEventCentral import db, create_app
from MusicEventCentral.models import *
app = create_app()
ctx = app.app_context()
ctx.push()
db.drop_all()
db.create_all()
quit()
