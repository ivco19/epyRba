# This file is part of the
#   Arcovid19 (https://ivco19.github.io/).
# Copyright (c) 2020, Arcovid Team
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/epyRba/master/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"After install commands"


# =============================================================================
# IMPORTS
# =============================================================================

from epyrba import flask_db


# =============================================================================
# LOGIC
# =============================================================================

def main():
    print("Creating tables")
    flask_db.database.create_tables(flask_db.Model.__subclasses__())


if __name__ == "__main__":
    main()
