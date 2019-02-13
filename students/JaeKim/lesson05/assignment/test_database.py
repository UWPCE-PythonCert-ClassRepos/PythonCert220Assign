import database as db
import pytest


@pytest.fixture(autouse=True)
def setup_teardown():
    ''' Fixture to execute before and after tests '''
    mongo = db.MongoDBConnection()
    with mongo:
        db = mongo.connection.get_database(name="db")

        # db.drop_collection("customers")
        # db.drop_collection("products")
        # db.drop_collection("rentals")

    yield

def test_show_rentals():
    print(assignment.database.cleanup())