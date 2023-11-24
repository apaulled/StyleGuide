from flask import Flask, request, render_template
from src.image_stuff import testy
import psycopg2
import os


app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='styleguide',
                            user='beyonce',
                            password='blue')
    return conn


@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from users;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    yuh = testy()
    return f"{yuh[0]} {yuh[1]} {yuh[2]} {users}"


if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=8000)
