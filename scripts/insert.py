import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

db_address = os.getenv('RDS_ADDRESS')
db_user = os.getenv('RDS_USER')
db_password = os.getenv('RDS_PASSWORD')
db_name = os.getenv('RDS_DB')

try:
    connection = mysql.connector.connect(
        host=db_address,
        user=db_user,
        password=db_password,
        database=db_name
    )

    if connection.is_connected():
        db_info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_info}")

        cursor = connection.cursor()

        # You can execute your queries here using the cursor
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"You're connected to the database: {record[0]}")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'connection' in locals():
        connection.close()
