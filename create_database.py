import datetime  # Import datetime for current date and time

def create_table(conn, table_name):
  """Creates a table with auto-incrementing S.No, datetime, and XY_coordinates."""
  # SQL statement to create a table if it doesn't exist
  create_table_sql = f"""
      CREATE TABLE IF NOT EXISTS {table_name} (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime DATETIME NOT NULL,
        X_coordinate INTEGER,
        Y_coordinate INTEGER
      );
  """
  try:
      # Execute the SQL statement
      conn.execute(create_table_sql)
      print("Table created successfully!")
  except Exception as e:
      print("Error creating table:", e)
  conn.commit()

def insert_data(conn, table_name, x_value, y_value):
  """Inserts data (current datetime and XY_coordinates) into the table."""
  # SQL statement to insert data into the table
  current_datetime = datetime.datetime.now()  # Get current datetime object
  insert_sql = f"""
      INSERT INTO {table_name} (datetime, X_coordinate, Y_coordinate)
      VALUES (?, ?, ?);
  """
  try:
      # Execute the SQL statement with parameters
      conn.execute(insert_sql, (current_datetime, x_value, y_value))
      # Commit the transaction
      conn.commit()
      print("Data inserted successfully!")
  except Exception as e:
      print("Error inserting data:", e)


    