import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host='ManuelGuillermoSanchez.mysql.pythonanywhere-services.com',
        user='ManuelGuillermoS',
        password='Python2024*.',
        database='ManuelGuillermoS$default',

    )
    return conn

