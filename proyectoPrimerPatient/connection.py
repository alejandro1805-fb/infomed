import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host='alejandro1805.mysql.pythonanywhere-services.com',
        user='alejandro1805',
        password='Fafb!1011089600',
        database='alejandro1805$claseInicial'
    )
    return conn

