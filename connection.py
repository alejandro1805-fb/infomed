import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host='ManuelSanchezB.mysql.pythonanywhere-services.com',
        user='ManuelSanchezB',
        password='Python2024*.',
        database='ManuelSanchezB$default',

    )
    return conn

