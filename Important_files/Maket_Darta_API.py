import pandas as pd
import psycopg2

# Update this to use an environment variable key
key = 'K9LODFVAXAA288I4'

# Replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = f'https://www.alphavantage.co/query?function=NATURAL_GAS&interval=daily&apikey={key}&datatype=csv'
df = pd.read_csv(url)

# Connection parameters
hostname = "localhost"  # Replace with your actual hostname or IP address
database = "Natural_Gas_API"  # Make sure the database name is correct
username = "postgres"
password = "Bomber4444!!"

try:
    # Establish a connection
    connection = psycopg2.connect(
        host=hostname, database=database, user=username, password=password
    )

    # If the connection was successful, print a message
    print("Connection successful!")

    # Create a cursor
    cursor = connection.cursor()

    # Example: Insert data into a table
# Example: Insert data into a table
# Example: Insert data into a table
# Example: Insert data into a table
    for index, row in df.iterrows():
        insert_query = "INSERT INTO defualt_hh_ng_api_data (date, price) VALUES (%s, %s)"  # Correct the table name here
        
        # Convert the "value" column from string to float, handling non-numeric values
        try:
            value = float(row["value"])
        except ValueError:
            value = None  # Set to None if value cannot be converted to float
        
        data_to_insert = (row["timestamp"], value)
        cursor.execute(insert_query, data_to_insert)




    # Commit changes and close cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

    # Print success message
    print("Data inserted successfully!")

except Exception as e:
    # If there's an exception, print an error message
    print("Connection or insertion failed:", e)
