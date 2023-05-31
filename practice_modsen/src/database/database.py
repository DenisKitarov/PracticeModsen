from src.config.cfg_parser import get_config
import psycopg2
import csv
import json
import datetime


class Database:
    def __init__(self):
        config = get_config('config.ini')
        db_settigs = config[config['database']['main']]
        self.connection = psycopg2.connect(host=db_settigs['host'], database=db_settigs['database'],
                                           user=db_settigs['user'], password=db_settigs['password'])

    def parse_to_db(self, filepath):

        format = '%Y-%m-%d %H:%M:%S'

        with open(filepath, 'r', encoding='UTF8') as csvfile, self.connection.cursor() as cursor:
            csv_reader = csv.reader(csvfile, delimiter=',')

            for row in csv_reader:
                text = row[0]
                try:
                    created_date = datetime.datetime.strptime(row[1], format)
                except:
                    print("incorrect date format, skipping row...")
                    continue

                try:
                    rubrics = json.loads(row[2].replace("'", '"'))
                except:
                    print("rubrics array is corrupted, skipping row...")
                    continue

                cursor.execute("INSERT INTO posts (rubrics, text, created_date) VALUES (ARRAY{2},'{0}','{1}')".format(
                    text.replace("'", "''"), created_date, rubrics))

        self.connection.commit()
        cursor.close()

    def delete_by_id(self, id):
        cursor = self.connection.cursor()

        cursor.execute("DELETE FROM posts WHERE posts.id = {}".format(id))

        self.connection.commit()
        cursor.close()

    def get_by_id(self, id):
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT id, text, created_date, rubrics FROM posts WHERE posts.id = {}".format(id))
        data = cursor.fetchone()
        if data == None or len(data) != 4:
            data = None
        else:
            data = {'id': data[0], 'text': data[1],
                    'created_date': data[2], 'rubrics': data[3]}

        cursor.close()
        return data
