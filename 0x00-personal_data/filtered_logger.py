#!/usr/bin/env python3

import logging
import re
import os
import sys
import mysql.connector
from typing import List

"""Regex-ing"""


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log message obfuscated.
    Args:
        fields (List[str]): fields to obfuscate
        redaction (str): replacement string for obfuscation
        message (str): log line
        separator (str): separator for each field
        Returns:
            str: obfuscated message
    """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message,
                            self.SEPARATOR)


PII_FIELDS = ("name", "email", "phone", "ssn", "ip")


def get_logger() -> logging.Logger:
    """Returns a logger object."""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(PII_FIELDS)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the secure holberton database."""
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.environ.get('PERSONAL_DATA_DB_NAME')

    conn = mysql.connector.connect(user=username, password=password,
                                   host=host, database=database)
    return conn


def main():
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM users"
    cursor.execute(query)
    for row in cursor:
        message = '; '.join([f"{k}={v}" for k, v in row.items()])
        logger.info(message)


if __name__ == '__main__':
    main()
