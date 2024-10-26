from Application import app, test_application
import pytest

#run the program
if (__name__ == "__main__"):
    #pytest.main()
    pytest.main(["--rootdir=./Application/"])
    #app.testing = True    
    #app.run(debug=True)
