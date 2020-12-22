import pandas as pd
import numpy as np
import mysql.connector
import pymysql


# Load data
df = pd.read_csv(
    "https://raw.githubusercontent.com/roberthryniewicz/datasets/master/airline-dataset/flights/flights.csv",
    low_memory=False,
)

def writeToDB(df,airports):
    cnx = mysql.connector.connect(user='bytechde', password='B100Franklin123',
                                  host='89.252.185.4',
                                  database='bytechde_airport_comp491')
    cursor = cnx.cursor()

    for line in df:
        print(line)


    time=dict["plane"]["end"].strftime('%Y-%m-%d %H:%M:%S')
    sqlite_select_query ="""INSERT INTO ground_operation (operation_id, plane_parked) VALUES (6, """+"'"+time+"')"


    cursor.execute(sqlite_select_query)

def getCSV():
    cnx = mysql.connector.connect(user='bytechde', password='B100Franklin123',
                                  host='89.252.185.4',
                                  database='bytechde_airport_comp491')
    cursor = cnx.cursor()

    """conn = pymysql.connect(host='89.252.185.4', user='bytechde',
                           password='B100Franklin123', database='bytechde_airport_comp491')
    cursor = conn.cursor()"""

    df_flight = pd.read_sql_query("""SELECT * FROM flight""", cnx)

    print(len(df_flight.index))


if __name__ == "__main__":
   getCSV()
