import os

QUESTIONS_RANDOM_FACTOR = 3
QUESTIONS_NUM_PER_SURVEY = 5

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_PARI_FILENAME = os.path.join(ROOT_DIR, 'tests/example.csv')

TEST = True
if TEST:
    DATABASE_URI = 'sqlite:///user_study.db'
else:
    MYSQL_USER = 'user_name'
    assert 'MYSQL_PASSWORD' in os.environ, "MYSQL_PASSWORD not in environment variables"
    MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
    MYSQL_ADDR = '127.0.0.1'
    MYSWL_DATABASE = 'user_study_example'
    DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_ADDR}/{MYSWL_DATABASE}'
