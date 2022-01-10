import sys
import os
from news_analyzer.database import Database


def export(user, password):
    # Check if the credentials are OK
    try:
        db = Database('localhost', user, password)

        # We don't need to reinvent the wheel here for exporting
        # mysql, so we just use the utility that comes with the
        # mysql installation
        os.system(
            f'mysqldump --user={user} --password={password} --result-file=dump.sql --databases news_analyzer')
    except:
        print('Database connection could not be established')


if __name__ == '__main__':
    # First argument: db user
    # Second: db password
    if len(sys.argv) < 3:
        print('ERROR: Please provide the database user and password')
        sys.exit()

    export(sys.argv[1], sys.argv[2])
