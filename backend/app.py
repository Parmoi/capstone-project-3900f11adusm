import json
from flask import Flask
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import db_manager as dbm

app = Flask(__name__)
password = os.environ['POSTGRES_PASSWORD']

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/widgets')
def get_widgets():
    conn = psycopg2.connect(
        host="db",
        user="postgres",
        password=password,
        database="example"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM widgets")

    row_headers=[x[0] for x in cursor.description]

    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()
    conn.close()

    return json.dumps(json_data)

@app.route('/initdb')
def db_init():
    dbm.database_setup()

    return 'Database has been setup successfully!'

@app.route('/insertcollector')
def db_collector_insert():
    dbm.insert_collector("bob@gmail.com", "bob728", "0444444444", "password", "home!", "placeholder")

    return 'Insert has been successful!'

@app.route('/updatecollector')
def db_collector_update():
    dbm.update_collector_info("bob728", "newtest@gmail.com", "bob1000", "0444444", "password", "home!22")

    return 'Update has been successful!'

if __name__ == "__main__":
    app.run(host ='0.0.0.0')
