import pytest
import argparse
import os

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

