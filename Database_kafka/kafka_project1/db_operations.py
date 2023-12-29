import mysql.connector as conn
from mysql.connector import errorcode

def get_highest_bid(db_config):
    try:
        # Establishing connection to the database using the provided configuration
        cnx = conn.connect(**db_config)
        cur = cnx.cursor()

        # Executing SQL query to find the maximum bid price
        cur.execute("SELECT MAX(price) FROM bid;")
        # Fetching the result of the query
        result = cur.fetchone()[0] or 0

        # Closing cursor and connection
        cur.close()
        cnx.close()

        # Returning the highest bid value
        return result
    except Exception as e:
        # Handling any exceptions that occur and printing an error message
        print(f"Database error: {e}")
        return 0

def insert_bid_record(db_config, name, price, bid_ts):
    try:
        # Establishing connection to the database using the provided configuration
        cnx = conn.connect(**db_config)
        cur = cnx.cursor()

        # SQL query to insert a new bid record
        query = "INSERT INTO bid (name, price, bid_ts) VALUES (%s, %s, %s)"
        data = (name, price, bid_ts)

        # Executing the query with the provided data
        cur.execute(query, data)
        # Committing the transaction to the database
        cnx.commit()

        # Getting the number of affected rows
        record_count = cur.rowcount

        # Closing cursor and connection
        cur.close()
        cnx.close()

        # Returning the number of inserted records
        return record_count
    except conn.Error as err:
        # Handling specific MySQL errors with custom messages
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None
