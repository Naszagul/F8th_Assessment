'''
Created by - Regan Preston

Unit Tests and Test Cases
F8th QA Engineer Assessment

This assessment was very eye-opening to me.  It is the first time
that I have ever created unit tests.  I had to do a lot of
research on FastAPI syntax, and the other working libraries included
on the main.py file to complete this task.

My approach to this assessment was to create test cases that test the
functionality of each application function (server_response(), sessions(),
and auth_check()).  For each function, I would provide it with a
set of data that I create.  Then I use the assert keyword to check
for an expected result against the dataset.

I was unable to figure out exactly how I should be passing data 
into my test cases as I am still new with some of the syntax.
However, I believe I was able to come up with a solution that showcases
my train of thought well.

One issue that was coming up for me, was that I had trouble running
pytest.  I was able to find a command that allows pytest to run:

py -3 -m pytest test_main.py     <--works for me    
pytest test_main.py              <--doesn't work for me

My test program does run, however there are probably a few logic errors.
When ran, my test_home() passes, but the other two test functions fail.

Thank you for giving me the opportunity to create this for you.  I was
able to learn a lot.  Feedback would be greatly appreciated.
'''

from fastapi.testclient import TestClient
from main import *

# create a test instance of app variable from main.py
test_app = TestClient(app)


# quick test to make sure home page is responding with status code 200
# also checking for content response equality
def test_home():
    response = test_app.get('/')
    assert response.status_code == 200
    assert response.json() == {"server": "ok"}


# testing sessions() function from main.
def test_sessions():

    # check multiple input data cases by creating an array of test case possibilities.
    data_cases = [
        # min expected valid case
        Sessions(timestamp=1, ip="1.1.1.1",
                 url="https://www.example.com/of/your/website?var=included"),
        # max expected valid case
        Sessions(timestamp=9999999999999, ip="192.168.10.2",
                 url="www.hello.com"),
        # expected invalid case
        Sessions(timestamp=1, ip=" ", url="")
    ]

    # iterating through each test data case, and asserting that the response status code
    # should equal 201 with a valid case.
    for case in data_cases:
        response = test_app.post(
            '/sessions/', data=case)

        # assuming 201 is the code to indicate function is working correctly.
        assert response.status_code == 201
        # I could also add test cases and assertions for the other status codes

# test auth_check()


def test_auth_check():

    # Following a similar scheme as my test_sessions() unit test.
    # create some data test cases to test against.
    data_cases = [
        # min field values
        AuthCheck(session_id=1, user_id="1",
                  policy={"risk": 1, "authenticity": 1, "web_bot": 1}),
        # max field values
        AuthCheck(session_id=294, user_id="Hi"*32,
                  policy={"risk": 100, "authenticity": 100, "web_bot": 100}),
        # invalid field values
        AuthCheck(session_id=5, user_id="", policy={"risk": -1, })
    ]

    test_count = 0
    for case in data_cases:
        response = test_app.post('/auth/check/', data=case)
        # check for 201 code where expected else expect invalid response code.
        assert response.status_code == 201 if test_count != 2 else response.status_code == 400
        test_count += 1
