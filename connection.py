import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host='ManuelGuillermoSanchez.mysql.pythonanywhere-services.com',
        user='ManuelGuillermoSanchez',
        password='Python2024*.',
        database='ManuelGuillermoSanchez$default',
        ssl_disabled=True  
    )
    return conn

