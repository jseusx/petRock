import psycopg2
from psycopg2 import Error
import pandas as pd
from main import Item, db

# this function is based on the tutorial at: https://pynative.com/python-postgresql-tutorial/
def connect_to_db(username='admin', password='root', host='127.0.0.1', port='5432', database='PetRock'):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(
            user=username,
            password=password,
            host=host,
            port=port,
            database=database
        )
        cursor = connection.cursor()
        print("connected to the database")

        return cursor, connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)


def disconnect_from_db(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed.")
    else:
        print("Connection does not work.")

   

def import_items_from_csv(csv_path):
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        item = Item(
            name=row['name'],
            description=row['description'],
            price=row['price']
        )
        db.session.add(item)
    
    db.session.commit()
    print("CSV data imported successfully.")