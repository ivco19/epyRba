import os
import datetime as dt
from io import StringIO

import sh

import pandas as pd

from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
from playhouse.sqlite_ext import *

from flask import Flask, render_template, make_response


# =============================================================================
# CONSTANTS
# =============================================================================

PRODUCTION = os.environ.get("EPYRBA_PRODUCTION", "").lower() == "true"

APP_DIR = os.path.dirname(os.path.realpath(__file__))

# The playhouse.flask_utils.FlaskDB object accepts database URL configuration.
DATABASE = (
    os.environ["EPYRBA_DATABASE"] if PRODUCTION else
    'sqliteext:///%s' % os.path.join(APP_DIR, 'epyrba.db'))

# if debug
DEBUG = not PRODUCTION


# The secret key is used internally by Flask to encrypt session data stored
# in cookies. Make this unique '
SECRET_KEY = os.environ["EPYRBA_SECRET"] if PRODUCTION else ""


# Create a Flask WSGI app and configure it using values from the module.
app = Flask(__name__)
app.config.from_object(__name__)

# FlaskDB is a wrapper for a peewee database that sets up pre/post-request
# hooks for managing database connections.
flask_db = FlaskDB(app)



# =============================================================================
# MODELS
# =============================================================================

class Cache(flask_db.Model):
    code = CharField(unique=True)
    content = TextField()
    timestamp = DateTimeField(default=dt.datetime.now, index=True)


# =============================================================================
# ROUTE
# =============================================================================

@app.route('/')
def download_csv():
    rver = sh.R(version=True)
    return rver


# =============================================================================
# MAIN
# =============================================================================

def main():
    # ~ flask_db.database.create_tables(safe=True)
    app.run(debug=True)

if __name__ == '__main__':
    main()
