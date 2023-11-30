from app import app
from app.models import *
from app import db
import os


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == '__main__':
    app.run(port=5000, debug=True)
