import sys
import os
from news_analyzer.database import Database


def export(user, password, dump_file):
    # Check if the credentials are OK
    try:
        db = Database('localhost', user, password)

        # We don't need to reinvent the wheel here for exporting
        # mysql, so we just use the utility that comes with the
        # mysql installation
        os.system(
            f'mysql –-user {user} –p news_analyzer --password={password} < {dump_file}')
    except:
        print('Database connection could not be established')


if __name__ == '__main__':
    # First argument: db user
    # Second: db password
    # Third: path to dump file
    if len(sys.argv) < 4:
        print('ERROR: Please provide the database user, password and the path to the dump file')
        sys.exit()

    export(sys.argv[1], sys.argv[2], sys.argv[3])
