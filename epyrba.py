import os
import datetime as dt
import hashlib
import json

import mistune

import sh

import jsonschema

from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
from playhouse.sqlite_ext import *

from flask import Flask, render_template, make_response, request


# =============================================================================
# CONSTANTS
# =============================================================================

PRODUCTION = os.environ.get("EPYRBA_PRODUCTION", "").lower() == "true"


APP_DIR = os.path.dirname(os.path.realpath(__file__))


TEMPLATES_AUTO_RELOAD = not PRODUCTION


# The playhouse.flask_utils.FlaskDB object accepts database URL configuration.
DATABASE = (
    os.environ["EPYRBA_DATABASE"] if PRODUCTION else
    'sqliteext:///%s' % os.path.join(APP_DIR, '_cache_epyrba.db'))


# if debug
DEBUG = not PRODUCTION


# The secret key is used internally by Flask to encrypt session data stored
# in cookies. Make this unique '
SECRET_KEY = os.environ["EPYRBA_SECRET"] if PRODUCTION else ""


# Create a Flask WSGI app and configure it using values from the module.
app = Flask(__name__)
app.config.from_object(__name__)


TTL = int(os.environ.get("EPYRBA_TTL", 60))


# FlaskDB is a wrapper for a peewee database that sets up pre/post-request
# hooks for managing database connections.
flask_db = FlaskDB(app)


README_PATH = os.path.join(APP_DIR, "README.md")


# =============================================================================
# JSON SCHEMA_
# =============================================================================

# check https://json-schema.org/
SCHEMA = {
    "type" : "object",
    "properties" : {
        'Time_to_death': {"type" : "number"},
        'fact_futuro': {"type" : "number"},
        'D_incbation': {"type" : "number"},
        'D_infectious': {"type" : "number"},
        'R0': {"type" : "number"},
        'R0p': {"type" : "number"},
        'D_recovery_mild': {"type" : "number"},
        'D_recovery_severe': {"type" : "number"},
        'D_hospital_lag': {"type" : "number"},
        'retardo': {"type" : "number"},
        'D_death': {"type" : "number"},
        'p_fatal': {"type" : "number"},
        'InterventionTime': {"type" : "number"},
        'InterventionAmt': {"type" : "number"},
        'p_severe': {"type" : "number"},
        "E0": {"type" : "number"},
        'duration': {"type" : "number"},
        'N': {"type" : "number"},
        'I0': {"type" : "number"},
        'timepoints': {
            "type": "array",
            "minItems": 1,
            "items": {"type": "number"}}
    }
}


DEFAULT_PAYLOAD = """
{
  "Time_to_death": 17,
  "fact_futuro": 0.5,
  "D_incbation": 5.2,
  "D_infectious": 2.9,
  "R0": 3.422,
  "R0p": 3.422,
  "D_recovery_mild": 5.1,
  "D_recovery_severe": 10.1,
  "D_hospital_lag": 5,
  "retardo": 4,
  "D_death": 14.1,
  "p_fatal": 0.021,
  "InterventionTime": 18,
  "InterventionAmt": 1.0,
  "p_severe": 0.2,
  "E0": 17.0,
  "duration": 30,
  "N": 440000.0,
  "I0": 1,
  "timepoints": [0, 1, 2, 3, 4]
}""".strip()


# =============================================================================
# R COMMANDS
# =============================================================================

SEIR_MODEL_PATH = os.path.join(APP_DIR, "seir_model.R")


seir_model = sh.Rscript.bake(SEIR_MODEL_PATH)


# =============================================================================
# MODELS
# =============================================================================

class Cache(flask_db.Model):
    code = CharField(unique=True)
    content = TextField()
    timestamp = DateTimeField(default=dt.datetime.now, index=True)

    @property
    def expired(self):
        now = dt.datetime.now()
        return (now - self.timestamp).seconds >= TTL


flask_db.database.create_tables(flask_db.Model.__subclasses__())


# =============================================================================
# ROUTE
# =============================================================================

@app.route('/')
def index():
    with open(README_PATH) as fp:
        src = fp.read().split("----", 1)[-1]

    footer = mistune.markdown(src)

    return render_template(
        "seir.html", dpayload=DEFAULT_PAYLOAD, footer=footer)


@app.route('/seir', methods=['POST'])
def seir():

    payload = json.loads(request.form["query"])

    # it the json is well formed
    jsonschema.validate(payload, SCHEMA)

    now = dt.datetime.now()

    query = json.dumps(payload)

    code = hashlib.sha1(
        str.encode(query, "utf8")
    ).hexdigest()

    cache = Cache.get_or_none(Cache.code == code)

    if cache is None:
        cache = Cache(code=code)
    if cache.content is None or cache.expired:
        cache.content = str(seir_model(query))
        cache.timestamp = now
    cache.save()

    output = make_response(cache.content)
    output.headers["Content-Disposition"] = (
        f"attachment; filename=export_{now.isoformat()}.csv")
    output.headers["Content-type"] = "text/csv"
    return output


# =============================================================================
# MAIN
# =============================================================================



if __name__ == '__main__':
    print("Please execute")
    print("\t$ export FLASK_APP=epyrba")
    print("and then run:")
    print("\t$ flask run")
