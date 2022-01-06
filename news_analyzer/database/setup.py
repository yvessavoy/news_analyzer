import sys
import os
from news_analyzer.database import Database

SETUP_FILES = [
    '01_create_db_and_tables',
    '02_create_views',
    '03_load_tables',
    '04_create_users',
]

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("ERROR: please specify user and password for database creation")
        sys.exit()

    user = sys.argv[1]
    pw = sys.argv[2]

    db = Database('localhost', user, pw)

    for sql in SETUP_FILES:
        print(f'Processing {sql}.sql...')

        with open(f'sql/{sql}.sql', 'r') as f:
            statements = f.read().split(";")
            for stmt in statements:
                if len(stmt) > 0:
                    db.connection.cursor().execute(stmt)

        print(f'Done with {sql}.sql')
