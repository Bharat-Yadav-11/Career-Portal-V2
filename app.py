from flask import Flask, Blueprint

from auth.routes import auth
from config import ApplicationConfig

from tests.database_test import mysql_test_database, redis_test_database

app = Flask(__name__)

# Register blueprint(s) for application modules
app.register_blueprint(auth, url_prefix="/auth")

# Application configuration
app.config.from_object(ApplicationConfig)
ApplicationConfig = ApplicationConfig()
  
# Test database connections
mysql_client = ApplicationConfig.mysql_client
redis_client = ApplicationConfig.redis_client

if not mysql_test_database(mysql_client)[0]:
    raise mysql_test_database(f"Unable to connect to MySQL database: {ApplicationConfig.mysql_host}")[1]

if not redis_test_database(redis_client)[0]:
    raise redis_test_database(f"Unable to connect to Redis database: {ApplicationConfig.redis_host}")[1]


mysql_cursor = mysql_client.cursor()


if __name__ == "__main__":
    app.run()
