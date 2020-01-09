from app import app
from flaskext.mysql import MySQL
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    database='cine',
    user='root',
    password='root')
conn.connect()

