""""
This file is used to store all the configuration variables for the application.
"""

import os
from dotenv import load_dotenv
import redis
import pymysql

load_dotenv()


class ApplicationConfig:
    """
    This class is used to store all the configuration variables for the application.
    Make sure to add the configuration variables in the .env file and load them using the dotenv library.
    """

    def __init__(self):
        # Application details
        self.app_name = "K.R. Mangalam University Career Portal"
        self.app_version = "1.0.0"
        self.app_authors = ["Om Mishra (https://github.com/om-mishra7/)","Yash Soni (https://github.com/yash-soni7744/)","Bharat Yadav (https://github.com/bharat-yadav-11/)","Shambhavi Singh (https://github.com/Shambhavisingh123/)"]

        self.app_contact_email = "contact@om-mishra.com"

        # Application configuration
        self.secret_key = os.getenv("SECRET_KEY")
        self.app_debug = (
            True if os.getenv("APPLICATION_ENVIRONMENT") == "development" else False
        )
        self.app_host = "0.0.0.0"

        # Database configuration
        self.redis_client = redis.from_url(os.getenv("REDIS_URI"))

        self.mysql_client = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor,
        db="career_portal",
        host=os.getenv("MYSQL_HOST"),
        password= os.getenv("MYSQL_PASSWORD"),
        read_timeout=5,
        port=27250,
        user=os.getenv("MYSQL_USER"),
        write_timeout=5,
        )
                

    def __str__(self):
        return f"Mini Project: {self.app_name} | Version: {self.app_version} | Authors: {', '.join(self.app_authors)} | Contact Email: {self.app_contact_email}"
