"""
This file contains the unit tests for the databases.
"""


def mongodb_test_database(mongodb_client):
    """
    Attempts to ping the MongoDB database to ensure that the connection is working.
    """
    try:
        mongodb_client.server_info()
        return (True, None)

    except Exception as error:
        return (False, error)


def redis_test_database(redis_client):
    """
    Attempts to ping the Redis database to ensure that the connection is working.
    """
    try:
        redis_client.ping()
        return (True, None)

    except Exception as error:
        return (False, error)
