from connection import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    for table in cursor:
        print(table)
    print("Conexión exitosa y tablas verificadas.")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")