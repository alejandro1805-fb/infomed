import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host='ManuelGuillermoSanchez.mysql.pythonanywhere-services.com',
        user='ManuelGuillermoSanchez',
        password='Python2024*.',
        database='ManuelGuillermoSanchez$default',
        ssl_ca='/etc/ssl/certs/ca-certificates.crt'  
    )
    return conn

