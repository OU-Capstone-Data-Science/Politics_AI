import pyodbc
import pandas as pd

server_name = 'datascienceforschool.cozlulgmmrar.us-east-2.rds.amazonaws.com'
user_name = 'boys'
password = 'rule'

# Inserts into database
def insert_database(query):

    # Connect to database
    conn = connect_database()

    # Create database cursor
    cursor = conn.cursor()

    # Execute insertion and commit to database
    cursor.execute(query)
    conn.commit()

    # Close connection
    disconnect_database(conn)


# Queries from Things Database and returns pandas table of results
def select_database(query):

    # Connect to database
    conn = connect_database()

    # Read query into table
    table = pd.read_sql_query(query, conn)

    # Close connection
    disconnect_database(conn)

    return table


# Connects to project database, change string to change database
def connect_database():

    # Connect to database and return connection
    return pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                          "Server=" + server_name +
                          ";Database=Things;"
                          ";UID=" + user_name +
                          ";PWD=" + password + ';'
                          )


# Disconnect from database
def disconnect_database(conn):

    conn.close()


if __name__ == "__main__":
    select = select_database("SELECT * FROM Candidate")
    print(select)