import uuid


def MySQLTestDatabase(connection):
    try:
        connection.ping()
        return (True, None)
    
    except Exception as error:
        return (False, error)


def RedisTestDatabase(connection):
    try:
        connection.ping()
        return (True, None)
    
    except Exception as error:
        return (False, error)