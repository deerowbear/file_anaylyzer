import sqlite3
import logging
import os


sqlite3.Binary = os.getcwd() + os.sep + "binary" + os.sep + "exiftool" + os.sep + "exiftool.exe"

logging.basicConfig(filename='database_manager.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
class DatabaseManager:
    def create_tables():
        sql_statements = [ 
            """CREATE TABLE IF NOT EXISTS photos (
                    id INTEGER PRIMARY KEY, 
                    file_name text NOT NULL,
                    create_date text NOT NULL,
                    file_size text NOT NULL,
                    x_resolution text NOT NULL,
                    y_resolution text NOT NULL,
                    source_path text NOT NULL,
                    destination_path text NOT NULL,
                    file_exits text NOT NULL,
                    is_copy text NOT NULL,
                    is_written text NOT NULL
            );"""]
        try:
            with sqlite3.connect('photos.db') as conn:
                cursor = conn.cursor()
                cursor.execute("DROP TABLE IF EXISTS photos")
                for statement in sql_statements:
                    cursor.execute(statement)
                conn.commit()
        except sqlite3.Error as e:
            logging.error(e)

    def write_date(values: str):
        try:
            with sqlite3.connect('photos.db') as conn:
                sql = '''INSERT INTO photos(file_name,create_date,file_size,x_resolution,y_resolution,source_path,destination_path,file_exits,is_copy,is_written)
                        VALUES(?,?,?,?,?,?,?,?,?,?) '''
                cursor = conn.cursor()
                cursor.execute(sql, (values))
                conn.commit()
        except sqlite3.Error as e:
            logging.error(e)

    def fetch_row(file_name: str):
        try:
            with sqlite3.connect('photos.db') as conn:
                cursor = conn.cursor()
                query = 'SELECT * FROM photos where file_name like \'%' + file_name + '%\'' + ' and file_exits = \'False\';'
                cursor.execute(query)
                rows = cursor.fetchall()
                conn.commit()
                return [dict(zip([key[0] for key in cursor.description], row)) for row in rows]
        except sqlite3.Error as e:
            logging.error(e)
            return ''

