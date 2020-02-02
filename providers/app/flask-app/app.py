from app import app

from app import app, db
from app.models import User, Post, Room

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Post': Post, 'Room': Room}

def ping():
return 'PONG', 200