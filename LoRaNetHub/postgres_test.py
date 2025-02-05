import psycopg2
from psycopg2 import sql
# from psycopg2.extras import execute_values

dbname="myproject"
dbtable="mytable"
user="postgres"
password="volleyboast"
host="localhost"
port="5432"

def insert_row(table, data):
    # Connect to PostgreSQL database
    try:
        connection = psycopg2.connect(
            dbname=dbname, 
            user=user, 
            password=password, 
            host=host, 
            port=port
        )
        cursor = connection.cursor()

        # Create the SQL INSERT query
        columns = data.keys()
        values = data.values()
        
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(map(sql.Placeholder, columns))
        )
        
        # Execute the insert query
        cursor.execute(insert_query, data)
        connection.commit()
        print(f"Row inserted into {table} successfully.")
    
    except Exception as e:
        print(f"Error inserting row: {e}")
    
    finally:
        if connection:
            cursor.close()
            connection.close()

def main():
    data = {
        'name': 'test2',
        'age': '456',
        # 'column3': 'value3',
    }
    insert_row(dbtable, data)

if __name__ == "__main__":
    main()