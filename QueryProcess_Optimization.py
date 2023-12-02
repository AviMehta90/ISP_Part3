import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time

def create_database(dbname):
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='akhila123'"
    conn = psycopg2.connect(conn_string)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Check if the database exists, drop it if it does
    cursor.execute(f"DROP DATABASE IF EXISTS {dbname};")

    #Code to create database
    sql_create_database = f"CREATE DATABASE {dbname};"
    cursor.execute(sql_create_database)
  
    print("Database has been created successfully!")
    conn.close()

def connect_postgres(dbname):
    conn_string = f"host='localhost' dbname={dbname} user='postgres' password='akhila123'"
    conn = psycopg2.connect(conn_string)
    return conn

def execute_schema_script(conn, script_path):
    with conn.cursor() as cursor:
        with open(script_path, 'r') as f:
            sql_script = f.read()
            cursor.execute(sql_script)
    conn.commit()
    print("Schema has been created successfully!")

def execute_insert_script(conn, script_path):
    with conn.cursor() as cursor:
        with open(script_path, 'r') as f:
            sql_script = f.read()
            cursor.execute(sql_script)
    conn.commit()
    print("Data has been inserted successfully!")
    
def retrieve_data(conn):
    
    cursor = conn.cursor()

    # Select data from the Products table
    cursor.execute(f"SELECT * FROM Products;")
    products_data = cursor.fetchall()
    print("Data from Products table:")
    for row in products_data:
        print(row)

    # Select data from the warehouses table
    cursor.execute(f"SELECT * FROM Warehouses;")
    warehouse_data = cursor.fetchall()
    print("\nData from warehouses table:")
    for row in warehouse_data:
        print(row)

def create_index(conn, index_name, table_name, column_name):
    with conn.cursor() as cursor:
        query = f"CREATE INDEX {index_name} ON {table_name} ({column_name});"
        cursor.execute(query)
    print(f"Index '{index_name}' created successfully!")

def example_query(conn, query_description, query):
    with conn.cursor() as cursor:
        start_time = time.time()
        cursor.execute(query)
        result = cursor.fetchall()
        print(query_description)
        print('\n'.join(str(a) for a in result))
        print("Time taken:", time.time() - start_time)

if __name__ == '__main__':
    dbname = "supply_chain"

    # Create the database
    create_database(dbname)

    # Connect to the newly created database
    conn = connect_postgres(dbname)

    # Specify the path to the SQL schema file
    schema_file_path = "schema.sql"

    # Execute the schema script to create tables
    execute_schema_script(conn, schema_file_path)

    # Specify the path to the SQL data insertion file
    insert_data_file_path = "insert_data.sql"

    # Execute the data insertion script
    execute_insert_script(conn, insert_data_file_path)
    
    #Retrieve the data 
    retrieve_data(conn)
    print()

    # Example 1: Creating Index on the ProductID column in the InventoryLevels table
    create_index(conn, "idx_inventory_product_id", "InventoryLevels", "ProductID")
    print()

    # Example 2: Query optimization using INNER JOIN
    example_query(conn, "Example 2 - INNER JOIN:",
                  """
                  SELECT il.WarehouseID, il.ProductID, il.QuantityOnHand, il.MinimumStockLevel, il.MaximumStockLevel, il.ReorderPoint,
                         p.ProductName, p.ProductDescription, p.Category, p.Price
                  FROM InventoryLevels il
                  INNER JOIN Products p ON il.ProductID = p.ProductID;
                  """)
    print()

    # Example 3: Query optimization using LEFT JOIN
    example_query(conn, "Example 3 - LEFT JOIN:",
                  """
                  SELECT il.WarehouseID, il.ProductID, il.QuantityOnHand, il.MinimumStockLevel, il.MaximumStockLevel, il.ReorderPoint,
                         p.ProductName, p.ProductDescription, p.Category, p.Price
                  FROM InventoryLevels il
                  LEFT JOIN Products p ON il.ProductID = p.ProductID;
                  """)
    print()

    # Example 4: Query optimization using WHERE clause and index
    example_query(conn, "Example 4 - WHERE clause with Index:",
                  """
                  SELECT ProductName, Price
                  FROM Products
                  WHERE Category = 'Electronics';
                  """)
    print()

    # Example 5: Query optimization using Aggregation
    example_query(conn, "Example 5 - Aggregation:",
                  """
                  SELECT WarehouseID, COUNT(*) as TotalProducts
                  FROM InventoryLevels
                  GROUP BY WarehouseID;
                  """)
    print()

    # Example 6: Query optimization using LIMIT
    example_query(conn, "Example 6 - LIMIT:",
                  """
                  SELECT OrderID, OrderDate, CustomerName
                  FROM Orders
                  ORDER BY OrderDate DESC
                  LIMIT 5;
                  """)
    print()

    # Example 7: Query optimization using EXISTS
    example_query(conn, "Example 7 - EXISTS:",
                  """
                  SELECT ProductName
                  FROM Products p
                  WHERE EXISTS (
                      SELECT 1
                      FROM InventoryLevels il
                      WHERE il.ProductID = p.ProductID
                  );
                  """)
    print()

    conn.close()
