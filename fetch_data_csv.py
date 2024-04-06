import csv

def fetch_data(conn, table_name, csv_filename="data.csv"):
  """Fetches all data from the specified table and stores it in a CSV file."""
  cursor = conn.cursor()
  cursor.execute(f"""SELECT * FROM {table_name}""")
  data = cursor.fetchall()  # Fetch all rows as a list of tuples

  # Open CSV file for writing (replace "data.csv" with your desired filename)
  with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write column names as the first row (optional)
    csv_writer.writerow([col[0] for col in cursor.description])  # Get column names
    csv_writer.writerows(data)  # Write data rows

  return data
