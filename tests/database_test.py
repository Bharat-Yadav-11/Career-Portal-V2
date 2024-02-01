"""
This file contains the unit tests for the databases.
"""


def mysql_test_database(mysql_client):
    """
    Attempts to ping the MySQL database to ensure that the connection is working.
    """
    try:
        mysql_client.ping()
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
