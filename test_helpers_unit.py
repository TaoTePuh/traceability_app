# test_helpers_unit.py

from utils.helpers import greet_user

def test_greet_user():
    assert greet_user("TaoTePuh") == "Hallo TaoTePuh, willkommen in der traceability_app!"
