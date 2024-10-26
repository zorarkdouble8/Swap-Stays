from Application import app
import pytest
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", action="store_true")
parser.add_argument("-p", "--production", action="store_true")

#run the program
if (__name__ == "__main__"):
    args = parser.parse_args()

    if (args.production == True):
        app.run()
    elif (args.test == True):
        pytest.main(["--rootdir=./Application/"])
    else:
        app.run(debug=True)

