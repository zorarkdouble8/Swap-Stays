import pytest
from Application import app, db # Ensure these imports point to your initialized app and db
from flask_migrate import Migrate 
import argparse
import os

migrate = Migrate(app, db)
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", action="store_true")
parser.add_argument("-p", "--production", action="store_true")

#run the program
if (__name__ == "__main__"):
    args = parser.parse_args()

    if (args.production == True):
        os.environ["TESTING"] = "False"
        from Application import app

        app.run()
    elif (args.test == True):
        os.environ["TESTING"] = "True"
        from Application import app

        pytest.main(["--rootdir=./Application/"])
    else:
        os.environ["TESTING"] = "False"
        from Application import app
        
        app.run(debug=True)

