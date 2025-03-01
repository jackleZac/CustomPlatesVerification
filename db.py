# This file handles MySQL connections and queries
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def get_all_plates():
    connection = get_db_connection()
    if not connection:
        return []
    cursor = connection.cursor()
    cursor.execute("SELECT plate_number FROM trucks")
    plates = [plate[0] for plate in cursor.fetchall()]
    cursor.close()
    connection.close()
    return plates

def add_truck_to_db(plate_number, truck_id, owner):
    connection = get_db_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO trucks (plate_number, truck_id, owner) VALUES (%s, %s, %s)",
                       (plate_number, truck_id, owner))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error adding truck to database: {e}")
        return False