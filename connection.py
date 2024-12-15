import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host='ManuelGuilleroSanchez.mysql.pythonanywhere-services.com',
        user='ManuelGuilleroSanchez',
        password='Python2024*.',
        database='ManuelGuilleroSanchez$default'
    )
    return conn

